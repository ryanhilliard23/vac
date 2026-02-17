import sys
import threading
import re
import datetime
import ctypes 
import os 
import glob 
import subprocess 
import queue
import requests
import json
import yt_dlp
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QHeaderView, QAbstractItemView, QToolButton, 
                               QMessageBox, QStyle, QSizePolicy, QFrame, 
                               QDialog, QCheckBox, QSlider, QLineEdit, QPushButton, QComboBox, QStackedLayout, QGridLayout)
from PySide6.QtCore import QObject, Signal, Slot, Qt, QSize, QTimer, QMimeData, QUrl, QPropertyAnimation, QRect, QEasingCurve, QPoint, QRectF
from PySide6.QtGui import QIcon, QFont, QFontDatabase, QColor, QDrag, QPixmap, QPainter, QPainterPath, QLinearGradient, QRegion
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from ui_index import Ui_MainWindow
import resources_rc
import core_convert
from history_manager import HistoryManager

APP_VERSION = "v1.0.0"

class StreamRedirector(QObject):
    text_written = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.buffer = ""
        
    def write(self, text):
        if not text: return
        self.buffer += text
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            if line.strip():
                self.text_written.emit(line)
        
        if len(self.buffer) > 80 and "Downloading" in self.buffer:
            self.text_written.emit(self.buffer)
            self.buffer = ""

    def flush(self):
        pass

class BackgroundService(QObject):
    finished_task = Signal(str) 
    
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = True
        
    def add_task(self, url, mode, quality):
        self.queue.put((url, mode, quality))

    def process_queue(self):
        while self.running:
            try:
                url, mode, quality = self.queue.get()
                self.run_download(url, mode, quality)
                self.queue.task_done()
                
                self.finished_task.emit(url) 
                
            except Exception as e:
                print(f"[SYSTEM] Queue Error: {e}")

    def run_download(self, url, mode, quality):
        is_url = url.lower().startswith('http')
        is_spotify = "open.spotify" in url.lower() or "http://googleusercontent.com/spotify.com" in url.lower()

        print(f"Starting process for: {url}")

        try:
            if is_spotify:
                print("Spotify link detected. Delegating to SpotDL engine...")
                core_convert.download_with_spotdl(url)
            
            elif not is_url:
                print(f"Search term detected: '{url}'")
                query = f"ytsearch1:{url} official audio"
                core_convert.download_media(url, mode='audio', search_query=query)
            
            else:
                core_convert.download_media(
                    url, 
                    mode=mode, 
                    max_height=quality
                )
                
        except Exception as e:
            print(f"Error occurred: {e}")

class MetadataFetcher(QObject):
    info_ready = Signal(str, str, str, QPixmap) 

    def fetch(self, url):
        threading.Thread(target=self._run_fetch, args=(url,), daemon=True).start()

    def _run_fetch(self, url):
        try:
            title = "Unknown Title"
            platform = "Web"
            duration = "--:--"
            thumb_url = ""

            if "spotify.com" in url.lower():
                platform = "Spotify"
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    r = requests.get(url, headers=headers, timeout=5)
                    html = r.text
                    
                    title_match = re.search(r'<meta property="og:title" content="(.*?)"', html)
                    img_match = re.search(r'<meta property="og:image" content="(.*?)"', html)
                    desc_match = re.search(r'<meta property="og:description" content="(.*?)"', html)
                    
                    artist_name = ""
                    if desc_match:
                        desc_text = desc_match.group(1)
                        if " · " in desc_text:
                            parts = desc_text.split(" · ")
                            artist_candidate = parts[0]
                            if "Spotify. " in artist_candidate:
                                artist_name = artist_candidate.split("Spotify. ")[-1].strip()
                            else:
                                artist_name = artist_candidate.strip()

                    if title_match: 
                        title = title_match.group(1)
                    if img_match: 
                        thumb_url = img_match.group(1)

                    if thumb_url and "i.scdn.co" in thumb_url:
                        thumb_url = re.sub(r'ab67616d0000[a-f0-9]{4}', 'ab67616d0000b273', thumb_url)

                    is_playlist = "/playlist/" in url.lower() or "/album/" in url.lower()
                    
                    if is_playlist:
                        duration = "Playlist"
                    elif title != "Unknown Title":
                        # Only search YouTube for duration if it is a Single Track
                        ydl_opts = {
                            'quiet': True,
                            'extract_flat': True, 
                            'noplaylist': True,
                            'ignoreerrors': True,
                        }
                        
                        if artist_name:
                            search_query = f"ytsearch1:{artist_name} - {title}"
                        else:
                            search_query = f"ytsearch1:{title}"
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(search_query, download=False)
                            if 'entries' in info and info['entries']:
                                video_data = info['entries'][0]
                                dur_sec = video_data.get('duration')
                                if dur_sec:
                                    m, s = divmod(dur_sec, 60)
                                    h, m = divmod(m, 60)
                                    if h > 0:
                                        duration = f"{int(h)}:{int(m):02d}:{int(s):02d}"
                                    else:
                                        duration = f"{int(m):02d}:{int(s):02d}"

                except Exception as e:
                    print(f"[METADATA] Spotify Hybrid Error: {e}")
                
                self._load_and_emit(title, platform, duration, thumb_url)
                return
            
            # YT-DLP 
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'skip_download': True,
                'ignoreerrors': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(url, download=False)
                if not data: return

                title = data.get('title', 'Unknown Title')
                
                extractor = data.get('extractor_key', 'Video')
                if 'youtube' in extractor.lower(): platform = "YouTube"
                elif 'soundcloud' in extractor.lower(): platform = "SoundCloud"
                else: platform = extractor

                dur_sec = data.get('duration')
                if dur_sec:
                    m, s = divmod(dur_sec, 60)
                    h, m = divmod(m, 60)
                    if h > 0:
                        duration = f"{int(h)}:{int(m):02d}:{int(s):02d}"
                    else:
                        duration = f"{int(m):02d}:{int(s):02d}"
                
                thumbnails = data.get('thumbnails', [])
                if thumbnails:
                    thumb_url = thumbnails[-1].get('url', '')
                else:
                    thumb_url = data.get('thumbnail', '')

                self._load_and_emit(title, platform, duration, thumb_url)

        except Exception as e:
            print(f"[METADATA ERROR] {e}")

    def _load_and_emit(self, title, platform, duration, thumb_url):
        pixmap = QPixmap()
        if thumb_url:
            try:
                r = requests.get(thumb_url, timeout=5)
                if r.status_code == 200:
                    pixmap.loadFromData(r.content)
            except Exception:
                pass
        
        self.info_ready.emit(title, platform, duration, pixmap)

class QueueItemWidget(QWidget):
    remove_clicked = Signal(object)

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedHeight(70) 
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(12)
        
        self.thumb_lbl = QLabel()
        self.thumb_lbl.setFixedSize(54, 54) 
        self.thumb_lbl.setStyleSheet("background-color: #333; border-radius: 6px;")
        self.thumb_lbl.setScaledContents(True)
        
        if data.get('pixmap') and not data['pixmap'].isNull():
            self.thumb_lbl.setPixmap(data['pixmap'])

        text_container = QWidget()
        text_container.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 4, 0, 4)
        text_layout.setSpacing(2)
        
        title_lbl = QLabel(data.get('title', 'Unknown'))
        title_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 12px; font-family: 'Manrope'; border: none;")
        
        fmt = data.get('mode', 'Video').upper()
        qual = data.get('quality')
        qual_str = f"{qual}p" if qual else "Best"
        meta_lbl = QLabel(f"{fmt} ({qual_str})")
        meta_lbl.setStyleSheet("color: #6b7280; font-size: 10px; font-family: 'JetBrains Mono'; border: none;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(meta_lbl)
        text_layout.addStretch()
        
        self.btn_remove = QToolButton()
        self.btn_remove.setText("✕")
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.setFixedSize(24, 24)
        self.btn_remove.clicked.connect(self.on_remove)
        self.btn_remove.setStyleSheet("""
            QToolButton { 
                background: transparent; 
                color: #ef4444; 
                font-weight: bold;
                border-radius: 12px;
                border: none;
            }
            QToolButton:hover { 
                background: rgba(239, 68, 68, 0.2); 
            }
        """)

        layout.addWidget(self.thumb_lbl)
        layout.addWidget(text_container, 1) 
        layout.addWidget(self.btn_remove)
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QueueItemWidget {
                /* Slightly lighter than the table background (#1c1c1e) to create a subtle card effect */
                background-color: #252527; 
                border: none; /* REMOVED THE BORDER */
                border-radius: 8px;
            }
        """)

    def on_remove(self):
        self.remove_clicked.emit(self.data)

class HistoryGridCard(QFrame):
    delete_requested = Signal(dict)
    play_requested = Signal(str)

    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.file_path = entry.get('file_path', '')
        self.drag_start_position = None
        
        # Load Thumbnail
        self.thumb_pixmap = None
        thumb_path = entry.get('thumb_path')
        if thumb_path and os.path.exists(thumb_path):
            self.thumb_pixmap = QPixmap(thumb_path)
        
        self.setFixedSize(280, 180) 
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("HistoryCard")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(4)

        self.top_row = QHBoxLayout()
        self.top_row.setSpacing(6)
        
        fmt_text = entry.get('format', 'FILE').upper()
        fname = entry.get('filename', '').lower()
        
        if "MP4" in fmt_text or "VIDEO" in fmt_text:
            icon_path = ":/images/video-camera-fill.png"
            if "4k" in fname or "2160p" in fname: badge_text = "4K"
            elif "1440p" in fname: badge_text = "2K"
            elif "720p" in fname: badge_text = "720p"
            else: badge_text = "1080p"
        else:
            icon_path = ":/images/music-note-fill.png"
            badge_text = "MP3"
        
        self.badge_widget = QWidget()
        self.badge_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.6); border-radius: 4px;")
        badge_layout = QHBoxLayout(self.badge_widget)
        badge_layout.setContentsMargins(6, 4, 8, 4)
        badge_layout.setSpacing(6)
        
        lbl_icon = QLabel()
        lbl_icon.setFixedSize(12, 12)
        lbl_icon.setScaledContents(True)
        lbl_icon.setStyleSheet("background: transparent; border: none;")
        pix = QPixmap(icon_path)
        if not pix.isNull(): lbl_icon.setPixmap(pix)
            
        lbl_text = QLabel(badge_text)
        lbl_text.setStyleSheet("color: white; font-weight: bold; font-size: 10px; font-family: 'Segoe UI'; border: none; background: transparent;")
        
        badge_layout.addWidget(lbl_icon)
        badge_layout.addWidget(lbl_text)
        
        dur_text = entry.get('duration', '--:--') 
        self.lbl_duration = QLabel(dur_text) 
        self.lbl_duration.setStyleSheet("background-color: rgba(0, 0, 0, 0.6); color: #d1d5db; border-radius: 4px; padding: 4px 8px; font-weight: 600; font-size: 10px;")

        self.top_row.addWidget(self.badge_widget)
        self.top_row.addStretch()
        self.top_row.addWidget(self.lbl_duration)
        self.layout.addLayout(self.top_row)
        self.layout.addStretch()

        # BOTTOM CONTENT 
        title_text = entry.get('filename', 'Unknown Title')
        self.lbl_title = QLabel(title_text)
        self.lbl_title.setWordWrap(True)
        self.lbl_title.setStyleSheet("color: white; font-weight: 800; font-size: 13px; font-family: 'Manrope', sans-serif; background: transparent;")
        self.layout.addWidget(self.lbl_title)

        # HOVER ACTIONS
        self.hover_container = QWidget()
        self.hover_layout = QHBoxLayout(self.hover_container)
        self.hover_layout.setContentsMargins(0, 8, 0, 0)
        self.hover_layout.setSpacing(8)

        size_text = entry.get('size', '-- MB')
        self.lbl_meta = QLabel(f"{size_text}")
        self.lbl_meta.setStyleSheet("color: #9ca3af; font-size: 11px; font-weight: 500; font-family: 'JetBrains Mono'; background: transparent;")
        
        def make_btn(icon_name, callback, tooltip, color=None):
            btn = QToolButton()
            btn.setIcon(QIcon(f":/images/{icon_name}"))
            btn.setIconSize(QSize(14, 14))
            btn.setFixedSize(28, 28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            base_style = "QToolButton { background-color: rgba(255,255,255,0.15); border-radius: 14px; border: none; }"
            hover_style = "QToolButton:hover { background-color: white; }"
            if color == "red":
                base_style = "QToolButton { background-color: rgba(239, 68, 68, 0.2); border-radius: 14px; border: none; color: #ef4444; font-weight: bold; }"
                hover_style = "QToolButton:hover { background-color: #ef4444; color: white; }"
                btn.setText("✕")
                btn.setIcon(QIcon())
            
            btn.setStyleSheet(base_style + hover_style)
            return btn

        self.btn_play = make_btn("play.png", self.action_play_internal, "Play in App")
        self.btn_folder = make_btn("folder-g.png", self.action_folder, "Show in Folder")
        self.btn_delete = make_btn("trash-wh", self.action_delete, "Delete", color="red")

        self.hover_layout.addWidget(self.lbl_meta)
        self.hover_layout.addStretch()
        self.hover_layout.addWidget(self.btn_play)
        self.hover_layout.addWidget(self.btn_folder)
        self.hover_layout.addWidget(self.btn_delete)

        self.layout.addWidget(self.hover_container)
        self.hover_container.hide()
        
        self.setStyleSheet("HistoryGridCard { background-color: #18181b; border: 1px solid #27272a; border-radius: 16px; }")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.drag_start_position:
            return
        
        # Ensure file actually exists before letting them drag it
        if not self.file_path or not os.path.exists(self.file_path):
            return

        # Check if the user moved the mouse far enough to count as a drag
        dist = (event.pos() - self.drag_start_position).manhattanLength()
        if dist < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        
        # This is the magic part: Convert file path to URL
        url = QUrl.fromLocalFile(self.file_path)
        mime_data.setUrls([url])
        drag.setMimeData(mime_data)

        # Create a semi-transparent ghost of the card to follow the mouse
        pixmap = self.grab()
        # Scale it down slightly (50%) so it's not huge while dragging
        scaled_pixmap = pixmap.scaled(self.width() // 2, self.height() // 2, 
                                    Qt.KeepAspectRatio, Qt.SmoothTransformation)
        drag.setPixmap(scaled_pixmap)
        drag.setHotSpot(event.pos() / 2)

        # Execute drag
        drag.exec(Qt.CopyAction)

    def enterEvent(self, event):
        self.hover_container.show()
        self.setStyleSheet("HistoryGridCard { background-color: #18181b; border: 1px solid #3B82F6; border-radius: 16px; }")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_container.hide()
        self.setStyleSheet("HistoryGridCard { background-color: #18181b; border: 1px solid #27272a; border-radius: 16px; }")
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform) 

        # Clip Corners
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 16, 16)
        painter.setClipPath(path)

        # Draw Background Image (Aspect Fill)
        if self.thumb_pixmap and not self.thumb_pixmap.isNull():
            target_rect = self.rect()
            img_size = self.thumb_pixmap.size()
            scale_w = target_rect.width() / img_size.width()
            scale_h = target_rect.height() / img_size.height()
            scale = max(scale_w, scale_h) 
            new_w = int(img_size.width() * scale)
            new_h = int(img_size.height() * scale)
            x = int((target_rect.width() - new_w) / 2)
            y = int((target_rect.height() - new_h) / 2)
            painter.drawPixmap(x, y, new_w, new_h, self.thumb_pixmap)
        else:
            painter.fillPath(path, QColor("#18181b")) 

        # Draw Gradient Overlay 
        grad = QLinearGradient(0, self.height() // 2, 0, self.height())
        grad.setColorAt(0.0, QColor(0, 0, 0, 0))
        grad.setColorAt(1.0, QColor(0, 0, 0, 240)) 
        painter.fillRect(self.rect(), grad)
        
        # Draw Slight Dark Tint 
        painter.fillRect(self.rect(), QColor(0, 0, 0, 40))

    def action_play_internal(self):
        if self.file_path and os.path.exists(self.file_path):
            self.play_requested.emit(self.file_path)

    def action_folder(self):
        if self.file_path:
            folder = os.path.dirname(self.file_path)
            if os.path.exists(folder): os.startfile(folder)

    def action_delete(self):
        self.delete_requested.emit(self.entry)
    
class RoundedThumbnail(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 56)
        self._pixmap = None

    def set_pixmap(self, pixmap):
        """Sets the pixmap and triggers a repaint."""
        self._pixmap = pixmap
        self.update()

    def clear(self):
        """Clears the image and triggers a repaint."""
        self._pixmap = None
        self.update()

    def paintEvent(self, event):
        """
        Custom paint event that handles high-quality scaling 
        and rounded corners dynamically.
        """
        if not self._pixmap or self._pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 6, 6)
        painter.setClipPath(path)

        target_rect = self.rect()
        img_size = self._pixmap.size()
        
        if img_size.width() == 0 or img_size.height() == 0: return

        # Calculate scale needed to cover the widget
        scale_w = target_rect.width() / img_size.width()
        scale_h = target_rect.height() / img_size.height()
        scale = max(scale_w, scale_h)
        
        new_w = int(img_size.width() * scale)
        new_h = int(img_size.height() * scale)
        
        # Center the image
        x = int((target_rect.width() - new_w) / 2)
        y = int((target_rect.height() - new_h) / 2)
        
        painter.drawPixmap(x, y, new_w, new_h, self._pixmap)

class ToastNotification(QFrame):
    def __init__(self, parent, title, message, type="info"):
        super().__init__(parent)
        self.setFixedSize(340, 78) # Sizing to match reference
        
        # Color Palettes
        styles = {
            "info":    {"border": "#3B82F6", "bg": "rgba(18, 18, 21, 0.95)", "icon": "i", "icon_bg": "#3B82F6"},
            "success": {"border": "#10B981", "bg": "rgba(16, 30, 20, 0.95)", "icon": "✓", "icon_bg": "#10B981"},
            "error":   {"border": "#EF4444", "bg": "rgba(35, 15, 15, 0.95)", "icon": "!", "icon_bg": "#EF4444"} 
        }
        
        current_style = styles.get(type, styles["info"])

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0) # Vertical centering handled by alignment
        layout.setSpacing(16)
        
        # Icon Circle
        self.icon_lbl = QLabel(current_style["icon"])
        self.icon_lbl.setFixedSize(28, 28)
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        self.icon_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {current_style['icon_bg']}; 
                color: white; 
                border-radius: 14px; 
                font-weight: 900; 
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                border: none;
            }}
        """)

        # Text Container
        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 16, 0, 16)
        text_layout.setSpacing(2)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: white; font-weight: 800; font-size: 15px; font-family: 'Manrope';")
        
        msg_lbl = QLabel(message)
        msg_lbl.setStyleSheet("color: #9ca3af; font-size: 12px; font-family: 'Manrope'; font-weight: 500;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(msg_lbl)
        
        layout.addWidget(self.icon_lbl)
        layout.addWidget(text_widget)
        
        # Card Styling
        self.setStyleSheet(f"""
            ToastNotification {{
                background-color: {current_style['bg']};
                border: 1px solid {current_style['border']}; 
                border-radius: 12px;
            }}
        """)
        
        # Slide Animation
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Auto-Close Timer (3.5 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_toast)
        self.timer.start(3500)
        
        self.show()

    def close_toast(self):
        # Slide down and destroy
        target = QPoint(self.x(), self.parent().height() + 10)
        self.anim.setEndValue(target)
        self.anim.setDirection(QPropertyAnimation.Forward)
        self.anim.finished.connect(self.close)
        self.anim.start()

class VideoContainer(QFrame):
    """
    A container that holds the video widget - fills available space.
    """
    mouse_activity = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("VideoContainer")
        self.setStyleSheet("""
            #VideoContainer {
                background-color: black;
            }
        """)
        self.setMouseTracking(True)
        
        self.video_widget = QVideoWidget(self)
        self.video_widget.setStyleSheet("background: black;")
        self.video_widget.setMouseTracking(True)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Make video widget fill the entire container
        self.video_widget.setGeometry(0, 0, self.width(), self.height())
        
    def mouseMoveEvent(self, event):
        self.mouse_activity.emit()
        super().mouseMoveEvent(event)

class MediaPlayerOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ref = parent
        self.setObjectName("MediaOverlay")
        self.hide()
        
        # Media Backend
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # LAYOUT STACK
        self.stack_layout = QStackedLayout(self)
        self.stack_layout.setStackingMode(QStackedLayout.StackOne)
        
        # VIDEO PLAYER
        self.video_page = QWidget()
        self.video_page.setObjectName("VideoPage")
        self.video_page.setStyleSheet("background-color: rgba(0, 0, 0, 0.85);")
        
        vp_layout = QVBoxLayout(self.video_page)
        vp_layout.setAlignment(Qt.AlignCenter)
        vp_layout.setContentsMargins(0, 0, 0, 0)
        
        # Card Size
        self.player_card = QFrame()
        self.player_card.setObjectName("PlayerCard")
        self.player_card.setFixedSize(960, 624) 
        self.player_card.setStyleSheet("background-color: black; border-radius: 12px; border: 1px solid #333;")
        
        card_layout = QVBoxLayout(self.player_card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # Video Widget 
        self.video_container = VideoContainer()
        self.video_container.mouse_activity.connect(self.show_controls)
        self.player.setVideoOutput(self.video_container.video_widget)
        self.video_container.video_widget.setStyleSheet(
            "background: black; border-top-left-radius: 12px; border-top-right-radius: 12px;"
        )
        card_layout.addWidget(self.video_container, 1)
        
        # Video Controls 
        self.video_controls_container = QFrame()
        self.video_controls_container.setObjectName("VideoControls")
        self.video_controls_container.setFixedHeight(84)
        self.video_controls_container.setStyleSheet("""
            #VideoControls {
                background-color: rgba(18, 18, 18, 0.95);
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            /* This strips the unwanted borders/backgrounds from labels/widgets */
            QLabel { background: transparent; border: none; }
            QWidget { background: transparent; border: none; }
        """)
        
        v_ctrl_layout = QVBoxLayout(self.video_controls_container)
        v_ctrl_layout.setContentsMargins(0, 10, 0, 10)
        v_ctrl_layout.setSpacing(4)
        
        # 1. Seek Slider
        v_slider_box = QWidget()
        v_slider_layout = QHBoxLayout(v_slider_box)
        v_slider_layout.setContentsMargins(20, 0, 20, 0)
        
        self.vid_slider = QSlider(Qt.Horizontal)
        self.vid_slider.setCursor(Qt.PointingHandCursor)
        self.vid_slider.sliderMoved.connect(self.set_position)
        self.vid_slider.setStyleSheet(self.get_slider_style())
        v_slider_layout.addWidget(self.vid_slider)
        
        v_ctrl_layout.addWidget(v_slider_box)
        
        # 2. Buttons Row
        v_btns_row = QHBoxLayout()
        v_btns_row.setContentsMargins(20, 0, 20, 4)
        v_btns_row.setSpacing(12)
        
        # Play Button (Reduced Size: 24x24)
        self.btn_vid_play = QToolButton()
        self.btn_vid_play.setFixedSize(24, 24)
        self.btn_vid_play.setCursor(Qt.PointingHandCursor)
        self.btn_vid_play.clicked.connect(self.toggle_playback)
        self.btn_vid_play.setStyleSheet(self.get_icon_style("play", False))

        # Volume Button (Reduced Size: 20x20)
        self.btn_vid_vol = QToolButton()
        self.btn_vid_vol.setFixedSize(20, 20)
        self.btn_vid_vol.setCursor(Qt.PointingHandCursor)
        self.btn_vid_vol.clicked.connect(self.toggle_mute)
        self.btn_vid_vol.setStyleSheet(self.get_icon_style("high", False))
        
        # Volume Slider
        self.vol_slider = QSlider(Qt.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(80)
        self.vol_slider.setFixedWidth(80)
        self.vol_slider.setCursor(Qt.PointingHandCursor)
        self.vol_slider.valueChanged.connect(self.set_volume)
        self.vol_slider.setStyleSheet(self.get_slider_style())
        
        # Time Label
        self.lbl_time_full = QLabel("0:00 / 0:00")
        self.lbl_time_full.setStyleSheet("color: #999; font-size: 11px; font-family: 'JetBrains Mono'; margin-left: 8px;")

        v_btns_row.addWidget(self.btn_vid_play)
        v_btns_row.addWidget(self.btn_vid_vol)
        v_btns_row.addWidget(self.vol_slider)
        v_btns_row.addWidget(self.lbl_time_full)
        v_btns_row.addStretch()
        
        # Meta Stack
        v_text_stack = QWidget()
        v_text_layout = QVBoxLayout(v_text_stack)
        v_text_layout.setContentsMargins(0, 0, 0, 0)
        v_text_layout.setSpacing(2)
        v_text_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.lbl_vid_title = QLabel("Video Title")
        self.lbl_vid_title.setStyleSheet("color: white; font-weight: bold; font-size: 13px; font-family: 'Manrope';")
        self.lbl_vid_title.setAlignment(Qt.AlignRight)
        
        self.lbl_vid_meta = QLabel("MP4 (4K)") 
        self.lbl_vid_meta.setStyleSheet("color: #3B82F6; font-size: 10px; font-family: 'JetBrains Mono'; font-weight: 600;")
        self.lbl_vid_meta.setAlignment(Qt.AlignRight)
        
        v_text_layout.addWidget(self.lbl_vid_title)
        v_text_layout.addWidget(self.lbl_vid_meta)
        
        # Close Button (Reduced: 20x20)
        self.btn_vid_close = QToolButton()
        self.btn_vid_close.setCursor(Qt.PointingHandCursor)
        self.btn_vid_close.setFixedSize(20, 20)
        self.btn_vid_close.clicked.connect(self.stop_and_hide)
        self.btn_vid_close.setStyleSheet(self.get_close_style())
        
        v_btns_row.addWidget(v_text_stack)
        v_btns_row.addSpacing(16)
        v_btns_row.addWidget(self.btn_vid_close)
        
        v_ctrl_layout.addLayout(v_btns_row)
        card_layout.addWidget(self.video_controls_container)
        vp_layout.addWidget(self.player_card)

        # 
        # AUDIO BAR (Updated to match Video Layout)
        self.audio_page = QFrame()
        self.audio_page.setObjectName("AudioBar")
        self.audio_page.setFixedHeight(84)
        self.audio_page.setStyleSheet("""
            #AudioBar {
                background-color: rgba(18, 18, 18, 0.95);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            /* Clean styles for audio mode too */
            QLabel { background: transparent; border: none; }
            QWidget { background: transparent; border: none; }
        """)
        
        # Use Vertical Layout to stack Slider on top of Buttons
        a_ctrl_layout = QVBoxLayout(self.audio_page)
        a_ctrl_layout.setContentsMargins(0, 10, 0, 10)
        a_ctrl_layout.setSpacing(4)
        
        # Seek Slider (Audio)
        a_slider_box = QWidget()
        a_slider_layout = QHBoxLayout(a_slider_box)
        a_slider_layout.setContentsMargins(20, 0, 20, 0)
        
        self.aud_slider = QSlider(Qt.Horizontal)
        self.aud_slider.setCursor(Qt.PointingHandCursor)
        self.aud_slider.sliderMoved.connect(self.set_position)
        self.aud_slider.setStyleSheet(self.get_slider_style())
        a_slider_layout.addWidget(self.aud_slider)
        
        a_ctrl_layout.addWidget(a_slider_box)
        
        # Buttons Row (Audio)
        a_btns_row = QHBoxLayout()
        a_btns_row.setContentsMargins(20, 0, 20, 4)
        a_btns_row.setSpacing(12)
        
        # Play Button
        self.btn_aud_play = QToolButton()
        self.btn_aud_play.setFixedSize(24, 24)
        self.btn_aud_play.setCursor(Qt.PointingHandCursor)
        self.btn_aud_play.clicked.connect(self.toggle_playback)
        self.btn_aud_play.setStyleSheet(self.get_icon_style("play", False))

        # Volume Button (New for Audio)
        self.btn_aud_vol = QToolButton()
        self.btn_aud_vol.setFixedSize(20, 20)
        self.btn_aud_vol.setCursor(Qt.PointingHandCursor)
        self.btn_aud_vol.clicked.connect(self.toggle_mute)
        self.btn_aud_vol.setStyleSheet(self.get_icon_style("high", False))
        
        # Volume Slider (New for Audio)
        self.aud_vol_slider = QSlider(Qt.Horizontal)
        self.aud_vol_slider.setRange(0, 100)
        self.aud_vol_slider.setValue(80)
        self.aud_vol_slider.setFixedWidth(80)
        self.aud_vol_slider.setCursor(Qt.PointingHandCursor)
        self.aud_vol_slider.valueChanged.connect(self.set_volume)
        self.aud_vol_slider.setStyleSheet(self.get_slider_style())
        
        # Time Label
        self.lbl_aud_time = QLabel("0:00 / 0:00")
        self.lbl_aud_time.setStyleSheet("color: #999; font-size: 11px; font-family: 'JetBrains Mono'; margin-left: 8px;")

        a_btns_row.addWidget(self.btn_aud_play)
        a_btns_row.addWidget(self.btn_aud_vol)
        a_btns_row.addWidget(self.aud_vol_slider)
        a_btns_row.addWidget(self.lbl_aud_time)
        a_btns_row.addStretch()
        
        # Meta Stack (Audio)
        a_text_stack = QWidget()
        a_text_layout = QVBoxLayout(a_text_stack)
        a_text_layout.setContentsMargins(0, 0, 0, 0)
        a_text_layout.setSpacing(2)
        a_text_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.lbl_aud_title = QLabel("Audio Title")
        self.lbl_aud_title.setStyleSheet("color: white; font-weight: bold; font-size: 13px; font-family: 'Manrope';")
        self.lbl_aud_title.setAlignment(Qt.AlignRight)
        
        self.lbl_aud_meta = QLabel("MP3 (HQ)") 
        self.lbl_aud_meta.setStyleSheet("color: #3B82F6; font-size: 10px; font-family: 'JetBrains Mono'; font-weight: 600;")
        self.lbl_aud_meta.setAlignment(Qt.AlignRight)
        
        a_text_layout.addWidget(self.lbl_aud_title)
        a_text_layout.addWidget(self.lbl_aud_meta)
        
        # Close Button
        self.btn_aud_close = QToolButton()
        self.btn_aud_close.setCursor(Qt.PointingHandCursor)
        self.btn_aud_close.setFixedSize(20, 20)
        self.btn_aud_close.clicked.connect(self.stop_and_hide)
        self.btn_aud_close.setStyleSheet(self.get_close_style())

        a_btns_row.addWidget(a_text_stack)
        a_btns_row.addSpacing(16)
        a_btns_row.addWidget(self.btn_aud_close)
        
        a_ctrl_layout.addLayout(a_btns_row)
        
        self.stack_layout.addWidget(self.video_page)
        self.stack_layout.addWidget(self.audio_page)

        # --- Backend Events ---
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.mediaStatusChanged.connect(self.handle_media_status)
        
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(350)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.is_video_mode = True
        self.is_muted = False

    # --- STYLE HELPERS ---
    def get_slider_style(self):
        return """
            QSlider::groove:horizontal { height: 4px; background: #333; border-radius: 2px; }
            QSlider::handle:horizontal { background: #fff; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }
            QSlider::sub-page:horizontal { background: #3B82F6; border-radius: 2px; }
        """
        
    def get_icon_style(self, name, is_blue_hover_only=False):
        # Generates CSS for tools (play, pause, high, low, muted)
        # name: 'play', 'pause', 'high', 'low', 'muted'
        return f"""
            QToolButton {{ background: transparent; border: none; image: url(:/images/{name}-white.png); }}
            QToolButton:hover {{ image: url(:/images/{name}-blue.png); }}
        """

    def get_close_style(self):
        return """
            QToolButton { background: transparent; border: none; image: url(:/images/x-bold.png); }
            QToolButton:hover { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
        """

    # UI UPDATERS 
    def update_play_icons(self, is_playing):
        style = self.get_icon_style("pause") if is_playing else self.get_icon_style("play")
        self.btn_vid_play.setStyleSheet(style)
        self.btn_aud_play.setStyleSheet(style)

    def update_vol_icons(self, volume):
        if self.is_muted or volume == 0: name = "muted"
        elif volume < 50: name = "low"
        else: name = "high"
        
        style = self.get_icon_style(name)
        self.btn_vid_vol.setStyleSheet(style)
        self.btn_aud_vol.setStyleSheet(style)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        vol = 0 if self.is_muted else self.vol_slider.value()
        self.audio_output.setVolume(vol / 100)
        self.update_vol_icons(vol)
            
    def set_volume(self, value):
        if self.is_muted: self.is_muted = False
        self.audio_output.setVolume(value / 100)
        # Sync sliders
        if self.vol_slider.value() != value: self.vol_slider.setValue(value)
        if self.aud_vol_slider.value() != value: self.aud_vol_slider.setValue(value)
        self.update_vol_icons(value)

    def play_media(self, file_path):
        if not os.path.exists(file_path): return
        if self.anim.state() == QPropertyAnimation.Running: self.anim.stop()
        try: self.anim.finished.disconnect()
        except: pass

        self.raise_() 
        self.show()

        # Detect Mode
        self.is_video_mode = file_path.lower().endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov'))
        
        # Metadata Detection
        filename = os.path.basename(file_path)
        display_name = os.path.splitext(filename)[0].replace('_', ' ')
        if len(display_name) > 55: display_name = display_name[:52] + "..."
        
        fmt = "MP4" if self.is_video_mode else "Audio"
        qual = "Standard"
        fn = filename.lower()
        if "4k" in fn or "2160" in fn: qual = "4K"
        elif "1440" in fn: qual = "2K"
        elif "1080" in fn: qual = "HD"
        elif "mp3" in fn: qual = "MP3"
        elif "flac" in fn: qual = "FLAC"
        
        meta_text = f"{fmt} ({qual})"
    
        self.lbl_vid_title.setText(display_name)
        self.lbl_vid_meta.setText(meta_text)
        self.lbl_aud_title.setText(display_name)
        self.lbl_aud_meta.setText(meta_text)

        # Geometry & Animation
        parent_w = self.parent_ref.width()
        parent_h = self.parent_ref.height()

        if self.is_video_mode:
            self.stack_layout.setCurrentWidget(self.video_page)
            self.setGeometry(0, parent_h, parent_w, parent_h)
            self.anim.setStartValue(QRect(0, parent_h, parent_w, parent_h)) 
            self.anim.setEndValue(QRect(0, 0, parent_w, parent_h)) 
        else:
            self.stack_layout.setCurrentWidget(self.audio_page)
            h = 84
            self.setGeometry(0, parent_h, parent_w, 0)
            self.anim.setStartValue(QRect(0, parent_h, parent_w, 0))        
            self.anim.setEndValue(QRect(0, parent_h - h, parent_w, h))

        self.player.setSource(QUrl.fromLocalFile(file_path))
        
        vol = self.vol_slider.value()
        self.audio_output.setVolume(vol / 100)
        self.update_vol_icons(vol)
        self.update_play_icons(True)
        
        self.player.play()
        self.anim.start()

    def toggle_playback(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.update_play_icons(False)
        else:
            self.player.play()
            self.update_play_icons(True)

    def stop_and_hide(self):
        self.player.stop()
        self.player.setSource(QUrl())
        self.update_play_icons(False)
        if self.anim.state() == QPropertyAnimation.Running: self.anim.stop()
        try: self.anim.finished.disconnect()
        except: pass

        current = self.geometry()
        parent_h = self.parent_ref.height()
        self.anim.setStartValue(current)
        if self.is_video_mode:
            self.anim.setEndValue(QRect(0, parent_h, self.width(), self.height()))
        else:
            self.anim.setEndValue(QRect(0, parent_h, self.width(), 0))
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def set_position(self, position):
        self.player.setPosition(position)

    def update_position(self, position):
        if not self.vid_slider.isSliderDown(): self.vid_slider.setValue(position)
        if not self.aud_slider.isSliderDown(): self.aud_slider.setValue(position)
        
        curr_s = (position // 1000)
        total_s = (self.player.duration() // 1000)
        time_str = f"{curr_s//60}:{curr_s%60:02} / {total_s//60}:{total_s%60:02}"
        
        self.lbl_time_full.setText(time_str)
        self.lbl_aud_time.setText(time_str)

    def update_duration(self, duration):
        self.vid_slider.setRange(0, duration)
        self.aud_slider.setRange(0, duration)
        self.update_position(self.player.position())

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia: self.update_play_icons(False)
    
    def show_controls(self): pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._is_first_show = True
        self.ui.btnFormatVideo.setCheckable(True)
        self.ui.btnFormatAudio.setCheckable(True)

        self.media_overlay = MediaPlayerOverlay(self) 
        self.media_overlay.raise_()

        self.cached_duration = "--:--"
        self.update_filter_styles("ALL")

        self.download_queue_data = []
        self.current_metadata_cache = {}
        self.setup_queue_table()
        
        # Connect Buttons
        if hasattr(self.ui, 'btnAddQueue'):
            self.ui.btnAddQueue.clicked.connect(self.add_to_queue)
            
        if hasattr(self.ui, 'btnClearQueue'):
            self.ui.btnClearQueue.clicked.connect(self.clear_queue)

        if hasattr(self.ui, 'btnAllMedia'):
            self.ui.btnAllMedia.clicked.connect(lambda: self.set_history_filter("ALL"))
            self.ui.btnAllMedia.setCheckable(True)
            self.ui.btnAllMedia.setChecked(True)
            
        if hasattr(self.ui, 'btnVideo'):
            self.ui.btnVideo.clicked.connect(lambda: self.set_history_filter("VIDEO"))
            self.ui.btnVideo.setCheckable(True)
            
        if hasattr(self.ui, 'btnAudio'):
            self.ui.btnAudio.clicked.connect(lambda: self.set_history_filter("AUDIO"))
            self.ui.btnAudio.setCheckable(True)

        # Connect the click signals to the set_mode function
        self.ui.btnFormatVideo.clicked.connect(lambda: self.set_mode('video'))
        self.ui.btnFormatAudio.clicked.connect(lambda: self.set_mode('audio'))
        self.meta_fetcher = MetadataFetcher()
        self.meta_fetcher.info_ready.connect(self.update_metadata_ui)

        self.input_timer = QTimer()
        self.input_timer.setSingleShot(True)
        self.input_timer.setInterval(50)
        self.input_timer.timeout.connect(self.trigger_metadata_fetch)

        # 1. CAPTURE ORIGINAL POSITIONS
        self.original_main_frame_y = self.ui.main_frame.y()
        self.original_main_frame_x = self.ui.main_frame.x()
        
        self.anim_pill = QFrame(self.ui.highlight_bar) 
        self.anim_pill.setObjectName("anim_pill")
        self.anim_pill.lower() 

        # Setup Animation
        self.nav_animation = QPropertyAnimation(self.anim_pill, b"geometry")
        self.nav_animation.setDuration(350) 
        self.nav_animation.setEasingCurve(QEasingCurve.InOutCubic)

        # Basic Setup
        if hasattr(self.ui, 'btnNavFiles'):
            self.ui.btnNavFiles.hide()

        self.setWindowTitle("VAC")
        self.setWindowIcon(QIcon(":/images/vac-logo.ico")) 

        self.current_mode = 'video'
        self.current_quality = None 
        self.is_downloading = False
        self.filter_state = "ALL" 
        self.last_download_title = "Unknown Title"

        self.history_manager = HistoryManager() 

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.progressBar.setValue(0)
        self.setup_metadata_ui()

        self.setup_nav_logic()
        self.setup_quality_buttons()
        self.setup_history_table() 
        self.populate_history_table() 
        
        self.ui.btnStartDownload.clicked.connect(self.start_download)
        
        try:
            self.ui.pasteBtn.clicked.connect(self.paste_from_clipboard)
            self.ui.urlInput.textChanged.connect(self.handle_input_change)
            self.ui.searchHistoryInput.textChanged.connect(self.apply_history_filters)
            self.ui.btnHistoryTrash.clicked.connect(self.clear_all_history)
            if hasattr(self.ui, 'btnSettings'):
                self.ui.btnSettings.clicked.connect(self.open_settings)
            self.ui.btnTotalDownloads.clicked.connect(self.reset_filters)
        except AttributeError:
            pass

        self.redirector = StreamRedirector()
        self.redirector.text_written.connect(self.update_console)
        sys.stdout = self.redirector 

        print("> System initialized. Waiting for input...")
        
        self.bg_service = BackgroundService()
        self.bg_service.finished_task.connect(self.handle_download_complete)
        
        self.thread = threading.Thread(target=self.bg_service.process_queue, daemon=True)
        self.thread.start()
        
        self.set_mode('video')
        self._meta_anim = None
        self._push_anim = None 

    def show_toast(self, title, message, type="info"):
        toast = ToastNotification(self.ui.centralwidget, title, message, type)
        
        # Position: Bottom Right
        pad_x = 24
        pad_y = 24
        target_x = self.width() - toast.width() - pad_x
        target_y = self.height() - toast.height() - pad_y
        
        # Start position
        start_y = self.height() + 10
        
        toast.move(target_x, start_y)
        
        toast.anim.setStartValue(QPoint(target_x, start_y))
        toast.anim.setEndValue(QPoint(target_x, target_y))
        toast.anim.start()

    def resizeEvent(self, event):
        # Keep the overlay at the bottom and full width
        if hasattr(self, 'media_overlay') and self.media_overlay.isVisible():
            current_h = self.media_overlay.height()
            self.media_overlay.setGeometry(0, self.height() - current_h, self.width(), current_h)
        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        if self._is_first_show:
            self.move_pill(self.ui.btnNavDashboard, immediate=True)
            self.ui.btnNavDashboard.setChecked(True)
            self._is_first_show = False
            
        # Restore from Minimize
        else:
            current_idx = self.ui.stackedWidget.currentIndex()
            if current_idx == 1:
                target_btn = self.ui.btnNavHistory
            else:
                target_btn = self.ui.btnNavDashboard
                
            self.move_pill(target_btn, immediate=True)

    def setup_metadata_ui(self):
        target_x = self.ui.inputContainer.x()
        target_y = self.ui.inputContainer.y() + self.ui.inputContainer.height() + 10
        self.ui.metadata_placeholder.move(target_x, target_y)
        self.ui.metadata_placeholder.setFixedWidth(941)
        self.ui.metadata_placeholder.setMinimumHeight(0) 
        self.ui.metadata_placeholder.setMaximumHeight(0) 
        self.ui.metadata_placeholder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.metadata_placeholder.show() 
        
        # Main Layout
        self.meta_layout = QHBoxLayout(self.ui.metadata_placeholder)
        self.meta_layout.setContentsMargins(0, 0, 0, 0)
        self.meta_layout.setSpacing(0)

        # Card Container
        container = QWidget()
        container.setObjectName("metaContainer")
        container.setStyleSheet("""
            #metaContainer {
                background-color: #0F0F12;
                border: 1px solid #333;
                border-left: 4px solid #3B82F6; /* Blue Accent */
                border-radius: 8px;
            }
        """)
        
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(16, 12, 16, 12)
        container_layout.setSpacing(16)

        # Thumbnail
        self.lbl_meta_thumb = RoundedThumbnail()
        self.lbl_meta_thumb.setStyleSheet("background-color: #222; border-radius: 6px;")
        
        # Text Info
        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0) 
        text_layout.setSpacing(4) 
        
        # Title
        self.lbl_meta_title = QLabel("Checking Link...")
        self.lbl_meta_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; font-family: 'Manrope';")
        
        # Subtitle Row (YouTube Icon • Time • Quality)
        sub_row = QWidget()
        sub_layout = QHBoxLayout(sub_row)
        sub_layout.setContentsMargins(0,0,0,0)
        sub_layout.setSpacing(8)
        
        self.lbl_platform = QLabel("▶ YouTube") 
        self.lbl_platform.setStyleSheet("""
            color: #9ca3af; 
            font-size: 11px; 
            font-family: 'JetBrains Mono'; 
            font-weight: 500;
        """)

        self.lbl_meta_desc = QLabel("•   --:--   •")
        self.lbl_meta_desc.setStyleSheet("color: #4b5563; font-size: 11px; font-family: 'JetBrains Mono';")

        self.lbl_quality_badge = QLabel("1080p60 Available")
        self.lbl_quality_badge.setStyleSheet("color: #10B981; font-size: 11px; font-family: 'JetBrains Mono'; font-weight: bold;")

        sub_layout.addWidget(self.lbl_platform)
        sub_layout.addWidget(self.lbl_meta_desc)
        sub_layout.addWidget(self.lbl_quality_badge)
        sub_layout.addStretch()
        
        text_layout.addWidget(self.lbl_meta_title)
        text_layout.addWidget(sub_row)

        # Close Button
        self.btn_close_meta = QToolButton()
        self.btn_close_meta.setText("✕")
        self.btn_close_meta.setCursor(Qt.PointingHandCursor)
        self.btn_close_meta.setStyleSheet("QToolButton { color: #666; font-size: 14px; background: transparent; border: none; } QToolButton:hover { color: white; }")
        self.btn_close_meta.clicked.connect(self.hide_metadata_card)

        container_layout.addWidget(self.lbl_meta_thumb)
        container_layout.addWidget(text_widget, 1) 
        container_layout.addWidget(self.btn_close_meta)

        self.meta_layout.addWidget(container)
        self.ui.metadata_placeholder.setStyleSheet("background: transparent; border: none;")

    def setup_queue_table(self):
        """Configures the table to look like a list."""
        if not hasattr(self.ui, 'queue_table'): return
        
        t = self.ui.queue_table
        t.setColumnCount(1)
        t.horizontalHeader().setVisible(False)
        t.verticalHeader().setVisible(False)
        t.setShowGrid(False)
        t.setFrameShape(QFrame.NoFrame)
        t.setSelectionMode(QAbstractItemView.NoSelection)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Styling with Custom Scrollbar
        t.setStyleSheet("""
            QTableWidget { 
                background: transparent; 
                border: none;
                outline: none;
            }
            QTableWidget::item { 
                background: transparent; 
                border: none;
                padding-bottom: 8px; 
            }
            
            /* --- Custom Scrollbar --- */
            QScrollBar:vertical {
                border: none;
                background: #0f0f12;
                width: 14px;
                margin: 15px 4px 15px 4px;
            }
            QScrollBar::handle:vertical {
                background: #2A2A30;
                min-height: 30px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3f3f46;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def save_cached_thumbnail(self, log_title):
        """
        Searches cache/queue for a matching title using fuzzy matching,
        saves the pixmap, and returns path.
        """
        target_pixmap = None
        log_title_clean = log_title.lower().strip()

        def is_match(cached_title):
            if not cached_title: return False
            c_title = cached_title.lower().strip()
            return (c_title in log_title_clean) or (log_title_clean in c_title)

        # Check Metadata Cache (Single Download)
        if is_match(self.current_metadata_cache.get('title')):
            target_pixmap = self.current_metadata_cache.get('pixmap')

        # Check Queue (Batch Download)
        if not target_pixmap:
            for item in self.download_queue_data:
                if is_match(item.get('title')):
                    target_pixmap = item.get('pixmap')
                    break
        
        # Save to Disk
        if target_pixmap and not target_pixmap.isNull():
            try:
                # Create thumbnails folder
                base_dir = core_convert.get_download_path()
                thumb_dir = os.path.join(base_dir, 'thumbnails')
                if not os.path.exists(thumb_dir):
                    os.makedirs(thumb_dir)
                
                # Sanitize filename
                safe_title = "".join([c for c in log_title if c.isalpha() or c.isdigit() or c==' ']).strip()
                save_path = os.path.join(thumb_dir, f"{safe_title}.jpg")
                
                target_pixmap.save(save_path, "JPG")
                return save_path
            except Exception as e:
                print(f"[ERROR] Failed to save thumbnail: {e}")
        
        return None

    def update_queue_ui(self):
        """Refreshes table rows and updates the count label."""
        t = self.ui.queue_table
        t.clear()
        t.setRowCount(len(self.download_queue_data))
        
        for row, data in enumerate(self.download_queue_data):
            # Create the custom widget
            item_widget = QueueItemWidget(data)
            item_widget.remove_clicked.connect(self.remove_from_queue)
            
            # Add to table
            t.setCellWidget(row, 0, item_widget)
            t.setRowHeight(row, 78)
            
        # Update Label
        count = len(self.download_queue_data)
        if hasattr(self.ui, 'download_queue'):
            self.ui.download_queue.setText(f"Conversion Queue • {count}")

    def add_to_queue(self):
        """Adds current input to the queue list."""
        url = self.ui.urlInput.text().strip()
        if not url: return

        # Use cached metadata or fallback
        title = self.current_metadata_cache.get('title', 'Unknown Title')
        pixmap = self.current_metadata_cache.get('pixmap', QPixmap())
        
        # Create Data Object
        item_data = {
            'id': len(self.download_queue_data) + 1, # Simple ID
            'url': url,
            'title': title,
            'pixmap': pixmap,
            'mode': self.current_mode,     # 'audio' or 'video'
            'quality': self.current_quality # e.g. 1080 or None
        }
        
        self.download_queue_data.append(item_data)
        self.update_queue_ui()
        
        # Visual Feedback
        self.show_toast("Added to Queue", f"{title[:20]}...", "success")
        
        # Optional: Clear input after adding
        self.ui.urlInput.clear()
        self.hide_metadata_card()

    def remove_from_queue(self, item_data):
        if item_data in self.download_queue_data:
            self.download_queue_data.remove(item_data)
            self.update_queue_ui()

    def clear_queue(self):
        self.download_queue_data = []
        self.update_queue_ui()

    def show_metadata_card(self, title, is_loading=False):
        """Expands the card to exactly 80px and pushes the main_frame down."""
        self.lbl_meta_title.setText(title)
        
        if is_loading:
            self.lbl_meta_desc.setText("Analyzing URL...")
            self.lbl_meta_thumb.clear()
        else:
            duration = getattr(self, 'cached_duration', '--:--')
            self.lbl_meta_desc.setText(f"•   {duration}   •")

        frame = self.ui.metadata_placeholder
        
        target_height = 80 
        current_height = frame.height()
        
        if abs(current_height - target_height) < 5 and current_height > 0:
            return

        frame.setFixedHeight(current_height) 

        if self._meta_anim and self._meta_anim.state() == QPropertyAnimation.Running:
            self._meta_anim.stop()

        self._meta_anim = QPropertyAnimation(frame, b"maximumHeight")
        self._meta_anim.setDuration(300)
        self._meta_anim.setStartValue(current_height)
        self._meta_anim.setEndValue(target_height)
        self._meta_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        def on_anim_finish():
            frame.setMaximumHeight(target_height) 
            frame.setMinimumHeight(target_height) 
            
        self._meta_anim.finished.connect(on_anim_finish)
        self._meta_anim.start()

        spacing = 0 
        push_distance = target_height + spacing 
        new_y_pos = self.original_main_frame_y + push_distance
        
        if self.original_main_frame_y < 10:
             new_y_pos = self.ui.main_frame.y() + push_distance

        if self._push_anim and self._push_anim.state() == QPropertyAnimation.Running:
            self._push_anim.stop()
            
        self._push_anim = QPropertyAnimation(self.ui.main_frame, b"pos")
        self._push_anim.setDuration(300)
        self._push_anim.setStartValue(self.ui.main_frame.pos())
        self._push_anim.setEndValue(QPoint(self.original_main_frame_x, new_y_pos))
        self._push_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._push_anim.start()

    def hide_metadata_card(self):
        """Collapses the card and pulls the main_frame up."""
        frame = self.ui.metadata_placeholder
        
        if self._meta_anim and self._meta_anim.state() == QPropertyAnimation.Running:
            self._meta_anim.stop()

        frame.setMinimumHeight(0) 

        self._meta_anim = QPropertyAnimation(frame, b"maximumHeight")
        self._meta_anim.setDuration(250)
        self._meta_anim.setStartValue(frame.height())
        self._meta_anim.setEndValue(0)
        self._meta_anim.setEasingCurve(QEasingCurve.InCubic)
        self._meta_anim.start()
        
        if self._push_anim and self._push_anim.state() == QPropertyAnimation.Running:
            self._push_anim.stop()
            
        self._push_anim = QPropertyAnimation(self.ui.main_frame, b"pos")
        self._push_anim.setDuration(250)
        self._push_anim.setStartValue(self.ui.main_frame.pos())
        self._push_anim.setEndValue(QPoint(self.original_main_frame_x, self.original_main_frame_y))
        self._push_anim.setEasingCurve(QEasingCurve.InCubic)
        self._push_anim.start()
        
        self.ui.urlInput.clear()

    def handle_input_change(self, text):
        clean_text = text.strip()
        
        # Detect Audio-Only Platforms
        is_audio_platform = "spotify" in clean_text.lower() or "soundcloud" in clean_text.lower()

        if is_audio_platform:
            # Disable Video Option if not already disabled
            if self.ui.btnFormatVideo.isEnabled():
                self.ui.btnFormatVideo.setEnabled(False)
                self.ui.btnFormatVideo.setToolTip("Video download not available for this platform")
            
            # Force switch to Audio Mode directly (No .click() simulation)
            if self.current_mode != 'audio':
                print("[GUI] Audio-only platform detected. Locking format to AUDIO.")
                self.set_mode('audio') 
        else:
            # Re-enable Video Option if it was disabled
            if not self.ui.btnFormatVideo.isEnabled():
                self.ui.btnFormatVideo.setEnabled(True)
                self.ui.btnFormatVideo.setToolTip("")

        if len(clean_text) > 8 and ("http" in clean_text or "www" in clean_text):
            if not self.ui.metadata_placeholder.isVisible():
                self.show_toast("URL Detected", "Fetching metadata...", type="info")
            
            self.show_metadata_card("Checking Link...", is_loading=True)
            self.input_timer.start()
            
        elif len(clean_text) == 0:
            self.hide_metadata_card()

    def trigger_metadata_fetch(self):
        url = self.ui.urlInput.text().strip()
        if url:
            print(f"[SYSTEM] Fetching metadata for: {url}")
            self.meta_fetcher.fetch(url)

    def update_dashboard_stats(self):
        """Calculates total storage and file counts."""
        history = self.history_manager.get_history()
        
        total_mb = 0.0
        vid_count = 0
        aud_count = 0
        
        for entry in history:
            # Calculate Storage
            size_str = entry.get('size', '0 MB')
            try:
                if "MB" in size_str:
                    val = float(size_str.replace(" MB", "").strip())
                    total_mb += val
                elif "GB" in size_str:
                     val = float(size_str.replace(" GB", "").strip())
                     total_mb += val * 1024
            except ValueError:
                pass

            # 2. Count Types
            fmt = entry.get('format', '').upper()
            if "MP4" in fmt or "VIDEO" in fmt:
                vid_count += 1
            else:
                aud_count += 1

        # Format storage: If > 1024 MB, show GB
        if total_mb > 1024:
            size_display = f"{total_mb/1024:.1f} GB"
        else:
            size_display = f"{total_mb:.1f} MB"

        if hasattr(self.ui, 'total_storage_label'):
            self.ui.total_storage_label.setText(size_display)
            
        if hasattr(self.ui, 'total_videos'):
            self.ui.total_videos.setText(str(vid_count))
            
        if hasattr(self.ui, 'total_audios'):
            self.ui.total_audios.setText(str(aud_count))

    def set_history_filter(self, mode):
        """Sets the filter state, updates UI buttons, and refreshes the grid."""
        self.filter_state = mode
        
        # Update the visual styles of the buttons
        self.update_filter_styles(mode)
            
        # Refresh the grid content
        self.populate_history_table()

    @Slot(str, QPixmap)
    def update_metadata_ui(self, title, platform, duration, pixmap):
        self.lbl_meta_title.setText(title)

        self.current_metadata_cache = {
            'title': title,
            'pixmap': pixmap,
            'url': self.ui.urlInput.text().strip()
        }
        self.cached_duration = duration
        # Update Platform Label
        icon_prefix = "▶ " if "YouTube" in platform else "♬ "
        self.lbl_platform.setText(f"{icon_prefix}{platform}")
        
        # Update Duration Label
        self.lbl_meta_desc.setText(f"•   {duration}   •")

        # Update Quality Label
        if self.current_quality is None:
            qual_text = "Best Quality Available"
        else:
            qual_text = f"{self.current_quality}p Selected"
        self.lbl_quality_badge.setText(qual_text)

        # Update Thumbnail
        if not pixmap.isNull():
            self.lbl_meta_thumb.set_pixmap(pixmap)
        else:
            pass

        # Show card if hidden
        if not self.ui.metadata_placeholder.height() > 0:
            self.show_metadata_card(title)

    @Slot(str)
    def update_console(self, text):
        clean_text = text.strip()
        if not clean_text: return

        if "[HISTORY_LOG]" in clean_text:
            try:
                data_part = clean_text.replace("[HISTORY_LOG]", "").strip()
                parts = data_part.split("::VAC::")
                
                title = parts[0]
                fmt = parts[1] if len(parts) > 1 else "MP4"
                given_path = parts[2] if len(parts) > 2 else ""
                
                # Duration
                raw_duration = parts[3] if len(parts) > 3 else "--:--"
                final_duration = self.cached_duration if (raw_duration == "--:--" or not raw_duration) else raw_duration
                
                # Thumbnail Path
                thumb_path = parts[4] if len(parts) > 4 else None
                if thumb_path == "None": thumb_path = None
                
                if not thumb_path:
                    thumb_path = self.save_cached_thumbnail(title)

                self.add_history_with_retry(title, fmt, given_path, final_duration, thumb_path, attempt=1)

            except Exception as e:
                print(f"Error logging history: {e}")
            return

        if "[PROGRESS]" in clean_text:
            try:
                val_str = clean_text.replace("[PROGRESS]", "").strip()
                self.ui.progressBar.setValue(int(val_str))
            except ValueError:
                pass
            return 

        if "[METADATA]" in clean_text:
            raw_title = clean_text.replace("[METADATA]", "").strip()
            self.last_download_title = raw_title
            
            if "Playlist:" in raw_title:
                clean_title = raw_title.replace("Playlist: ", "")
                self.show_metadata_card(clean_title)
            else:
                self.show_metadata_card(raw_title)
            return 
        
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        formatted_msg = f"{timestamp} {clean_text}"
        self.ui.consoleLog.append(formatted_msg)

    def add_history_with_retry(self, title, fmt, given_path, duration, thumb_path, attempt=1):
        final_path = None
        final_size = "Unknown"

        if given_path and os.path.exists(given_path):
            final_path = given_path
            try:
                final_size = f"{os.path.getsize(final_path) / (1024*1024):.1f} MB"
            except:
                pass
        
        elif not given_path: 
             download_root = core_convert.get_download_path()
             sub = 'mp3' if 'MP3' in fmt else 'mp4'
             target_folder = os.path.join(download_root, sub)
             final_path, final_size = self.get_latest_file_info(target_folder)

        if final_path:
            url = self.ui.urlInput.text()
            self.history_manager.add_entry(
                filename=title, 
                url=url, 
                fmt=fmt, 
                size=final_size, 
                file_path=final_path,
                duration=duration,
                thumb_path=thumb_path,
                status="Completed"
            )
            self.populate_history_table()
            print(f"[SYSTEM] History added: {final_path}")
        else:
            if attempt < 10:
                QTimer.singleShot(1000, lambda: self.add_history_with_retry(title, fmt, given_path, attempt+1))
            else:
                print(f"[ERROR] Could not find file after 10s: {title}")

    def start_download(self):
        # 1. Check if Queue has items
        if self.download_queue_data:
            count = len(self.download_queue_data)
            self.show_toast("Batch Started", f"Processing {count} items...", "info")
            
            self.is_downloading = True
            self.ui.btnStartDownload.setEnabled(False)
            self.ui.progressBar.show()
            self.ui.consoleLog.clear()
            
            # Send all tasks to background service
            for item in self.download_queue_data:
                print(f"[BATCH] Queuing: {item['title']}")
                self.bg_service.add_task(item['url'], item['mode'], item['quality'])
            return

        # If Queue is empty
        url = self.ui.urlInput.text().strip()
        if not url:
            self.show_toast("Error", "Please enter a valid URL or add items to queue.", "error")
            return

        if self.is_downloading:
            self.show_toast("Warning", "A download is currently in progress.", "error")
            return

        self.is_downloading = True
        self.last_download_title = "Unknown Title"
        self.ui.btnStartDownload.setEnabled(False)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self.ui.consoleLog.clear()
        
        self.show_toast("Started", "Initializing download...", "info")
        self.bg_service.add_task(url, self.current_mode, self.current_quality)

    @Slot(str)
    def handle_download_complete(self, url):
        # Try to find the finished URL in our queue data
        found_in_queue = False
        
        # Iterate over a copy [:] so we can modify the original list safely
        for item in self.download_queue_data[:]: 
            if item['url'] == url:
                self.download_queue_data.remove(item)
                found_in_queue = True
                break # Remove only one instance (in case of duplicates)
        
        if found_in_queue:
            self.update_queue_ui()

            if not self.download_queue_data:
                # Batch is fully done
                self.is_downloading = False
                self.ui.btnStartDownload.setEnabled(True)
                self.ui.progressBar.setValue(100)
                self.show_toast("Batch Complete", "All items processed successfully.", "success")
            else:
                self.show_toast("Item Finished", "Removed from queue.", "success")
                
        # Single Download Mode
        else:
            self.is_downloading = False
            self.ui.btnStartDownload.setEnabled(True)
            self.ui.progressBar.setValue(100)
            self.show_toast("Success", "Download completed successfully.", "success")

    def closeEvent(self, event):
        self.bg_service.running = False 
        sys.stdout = sys.__stdout__
        event.accept()

    def setup_history_table(self):
        try:
            table = self.ui.download_history_table
            
            # Set Columns
            table.setColumnCount(3)
            
            # Hide Headers & Borders
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.setShowGrid(False)
            table.setFrameShape(QFrame.NoFrame)
            
            # Styling
            table.setStyleSheet("""
                QQTableWidget {
                    background-color: transparent;
                    border: none;
                    
                }
                QTableWidget::item {
                    background-color: transparent;
                    border: none;
                    
                }
                
                /* --- Custom Scrollbar --- */
                QScrollBar:vertical {
                    border: none;
                    background: #0f0f12;
                    width: 14px;
                    margin: 15px 4px 15px 4px;
                }
                QScrollBar::handle:vertical {
                    background: #2A2A30;
                    min-height: 30px;
                    border-radius: 3px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #3f3f46;
                }
                QScrollBar::add-line:vertical, 
                QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar::add-page:vertical, 
                QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)

            # 4. Header Sizing (CRITICAL FIX FOR OVERLAP)
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setMinimumSectionSize(300)
            
            # Interaction
            table.setSelectionMode(QAbstractItemView.NoSelection)
            table.setFocusPolicy(Qt.NoFocus)

        except AttributeError:
            print("[DEBUG] Warning: 'download_history_table' not found.")

    def update_total_downloads_button(self):
        if hasattr(self.ui, 'btnTotalDownloads'):
            count = len(self.history_manager.get_history())
            self.ui.btnTotalDownloads.setText(f"({count} Items)")

    def toggle_history_filter(self):
        if self.filter_state == "ALL":
            self.filter_state = "VIDEO"
            self.ui.btnFilterHistory.setToolTip("Filter: Video Only")
        elif self.filter_state == "VIDEO":
            self.filter_state = "AUDIO"
            self.ui.btnFilterHistory.setToolTip("Filter: Audio Only")
        else:
            self.filter_state = "ALL"
            self.ui.btnFilterHistory.setToolTip("Filter: All Files")
        self.apply_history_filters()

    def reset_filters(self):
        self.filter_state = "ALL"
        if hasattr(self.ui, 'searchHistoryInput'):
            self.ui.searchHistoryInput.clear()
        self.apply_history_filters()

    def apply_history_filters(self):
        self.populate_history_table()

    def play_file(self, file_path):
        if file_path and os.path.exists(file_path):
            try:
                os.startfile(file_path)
                print(f"[SYSTEM] Opening: {file_path}")
            except Exception as e:
                print(f"[ERROR] Could not open file: {e}")
                QMessageBox.warning(self, "Error", f"Could not open file:\n{e}")
        else:
            print(f"[ERROR] File not found: {file_path}")
            QMessageBox.warning(self, "File Not Found", "The file has been moved or deleted.")

    def open_folder_location(self, path):
        if not os.path.exists(path):
            print(f"Error: Path not found: {path}")
            return
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

    def delete_history_item(self, entry):
        # 1. Delete Main Media File
        file_path = entry.get('file_path')
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[SYSTEM] Deleted file: {file_path}")
            except Exception as e:
                print(f"[ERROR] Could not delete file: {e}")
        else:
            print(f"[SYSTEM] File not found on disk: {entry}")

        # Delete Thumbnail File
        thumb_path = entry.get('thumb_path')
        if thumb_path and os.path.exists(thumb_path):
            try:
                os.remove(thumb_path)
                print(f"[SYSTEM] Deleted thumbnail: {thumb_path}")
            except Exception as e:
                print(f"[ERROR] Could not delete thumbnail: {e}")

        # Remove from JSON and UI
        self.history_manager.delete_entry(entry)
        self.populate_history_table()

    def clear_all_history(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Clear History")
        msg.setText("Are you sure you want to delete all history?")
        msg.setInformativeText("This will permanently delete all downloaded files and thumbnails from your disk.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        msg.setStyleSheet("QMessageBox {background-color: #1e1e1e; color: white;} QLabel {color: white;}")

        if msg.exec() == QMessageBox.Yes:
            data = self.history_manager.get_history()
            deleted_count = 0
            
            for entry in data:
                # Delete Main File
                file_path = entry.get('file_path')
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"[ERROR] Could not delete {file_path}: {e}")

                # Delete Thumbnail
                thumb_path = entry.get('thumb_path')
                if thumb_path and os.path.exists(thumb_path):
                    try:
                        os.remove(thumb_path)
                    except Exception as e:
                        print(f"[ERROR] Could not delete thumbnail {thumb_path}: {e}")
            
            print(f"[SYSTEM] Bulk delete complete. Removed {deleted_count} media files")
            self.history_manager.clear_history()
            self.populate_history_table()

    def populate_history_table(self):
        if not hasattr(self.ui, 'download_history_table'): return
        
        table = self.ui.download_history_table
        table.clearContents() 
        
        # Get all data
        all_data = self.history_manager.get_history()
        
        # Filter Data (Search + Type)
        search_query = ""
        if hasattr(self.ui, 'searchHistoryInput'):
            search_query = self.ui.searchHistoryInput.text().lower().strip()
            
        filtered_data = []
        for entry in all_data:
            name_text = entry.get('filename', '').lower()
            if search_query and search_query not in name_text:
                continue
            
            # Type Filter logic
            fmt_text = entry.get('format', '').upper()
            if self.filter_state == "VIDEO" and ("MP3" in fmt_text or "AUDIO" in fmt_text): continue
            elif self.filter_state == "AUDIO" and ("MP4" in fmt_text or "VIDEO" in fmt_text): continue

            filtered_data.append(entry)

        # Calculate Grid Size
        total_items = len(filtered_data)
        columns = 3
        rows_needed = (total_items + columns - 1) // columns
        
        table.setRowCount(rows_needed)

        # Fill the Grid with Spaced Wrappers
        for index, entry in enumerate(filtered_data):
            row = index // columns
            col = index % columns
            
            container = QWidget()
            container.setStyleSheet("background: transparent;") # Invisible container
            
            # Layout with Margins = THE GAP
            layout = QVBoxLayout(container)
            layout.setContentsMargins(10, 10, 10, 10) # 10px gap on all sides
            layout.setAlignment(Qt.AlignCenter)
            
            # Create the actual card
            card = HistoryGridCard(entry)
            card.play_requested.connect(self.media_overlay.play_media)
            card.delete_requested.connect(lambda e=entry: self.delete_history_item(e))
            layout.addWidget(card)
            
            # Set into table
            table.setCellWidget(row, col, container)
            table.setRowHeight(row, 200)

        self.update_total_downloads_button()
        self.update_dashboard_stats()

    def truncate_text(self, text, max_len=60):
        if len(text) > max_len:
            return text[:max_len-3] + "..."
        return text

    def update_filter_styles(self, mode):
        """Applies active/inactive CSS to filter buttons based on current mode."""
        
        # --- CSS Definitions ---
        active_style = """
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
                font-family: 'Manrope';
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """
        
        inactive_style = """
            QPushButton {
                background-color: rgb(28, 28, 30);
                color: #9ca3af;
                border: 1px solid rgba(255, 255, 255, 12);
                border-radius: 15px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
                font-family: 'Manrope';
            }
            QPushButton:hover {
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                background-color: #18181b;
            }
            QPushButton:pressed {
                background-color: #27272a;
            }
        """
        
        # Media Button
        if hasattr(self.ui, 'btnAllMedia'):
            if mode == "ALL":
                self.ui.btnAllMedia.setStyleSheet(active_style)
            else:
                self.ui.btnAllMedia.setStyleSheet(inactive_style)

        # Video Button
        if hasattr(self.ui, 'btnVideo'):
            if mode == "VIDEO":
                self.ui.btnVideo.setStyleSheet(active_style)
            else:
                self.ui.btnVideo.setStyleSheet(inactive_style)

        # Audio Button
        if hasattr(self.ui, 'btnAudio'):
            if mode == "AUDIO":
                self.ui.btnAudio.setStyleSheet(active_style)
            else:
                self.ui.btnAudio.setStyleSheet(inactive_style)

    # ADD CARD WIDGET TO TABLE
    def add_history_row_visual(self, entry):
        self.populate_history_table()

    def get_latest_file_info(self, folder_path):
        try:
            if not os.path.exists(folder_path): return (None, "--")
            files = glob.glob(os.path.join(folder_path, "*"))
            
            valid_files = [f for f in files if ".part" not in f and not re.search(r'\.f[0-9]+', f)]
            
            if not valid_files: return (None, "--")
            
            latest_file = max(valid_files, key=os.path.getctime)
            size_bytes = os.path.getsize(latest_file)
            size_mb = size_bytes / (1024 * 1024)
            return (latest_file, f"{size_mb:.1f} MB")
        except Exception:
            return (None, "--")

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.ui.urlInput.setText(text)
            print("Pasted link from clipboard.")

    def select_quality(self, selected_btn, quality_val):
        self.current_quality = quality_val
        for btn in self.quality_map.keys():
            if btn != selected_btn:
                btn.setChecked(False)
        label = "Best" if quality_val is None else f"{quality_val}p"
        print(f"Quality setting updated: {label}")

    def set_mode(self, mode):
        self.current_mode = mode
        print(f"Format switched to: {mode.upper()}")
        
        # Visual Toggle
        if mode == 'video':
            self.ui.btnFormatVideo.setChecked(True)
            self.ui.btnFormatAudio.setChecked(False)
            is_video = True
        else:
            self.ui.btnFormatVideo.setChecked(False)
            self.ui.btnFormatAudio.setChecked(True)
            is_video = False

        # Disable Quality Controls if Audio is selected
        if hasattr(self.ui, 'comboQuality'):
            self.ui.comboQuality.setEnabled(is_video)
            
        if hasattr(self.ui, 'btnQualBest'):
            self.ui.btnQualBest.setEnabled(is_video)

        # Update the Metadata Badg
        if hasattr(self, 'lbl_quality_badge'):
            if not is_video:
                self.lbl_quality_badge.setText("Audio Quality: High")
            else:
                # Restore previous video state
                if self.current_quality:
                    self.lbl_quality_badge.setText(f"{self.current_quality}p Selected")
                else:
                    self.lbl_quality_badge.setText("Best Quality Available")

    def setup_nav_logic(self):
        self.nav_buttons = [
            (self.ui.btnNavDashboard, 0),
            (self.ui.btnNavHistory, 1)
        ]
        for btn, index in self.nav_buttons:
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, b=btn, i=index: self.switch_page(b, i))

    def switch_page(self, active_btn, index):
        """Switches page and triggers the pill animation"""
        self.ui.stackedWidget.setCurrentIndex(index)
        
        # Update styling state for text colors
        for btn, _ in self.nav_buttons:
            btn.setChecked(btn == active_btn)

        # Animate the pill to the new button
        self.move_pill(active_btn)

    def move_pill(self, target_button, immediate=False):
        """Calculates dynamic radius and expands size with padding"""
        target_geometry = target_button.geometry()
 
        h_padding = 0  # Widen
        v_padding = 10   # Tallness
        
        # Apply the padding to the geometry
        padded_geometry = target_geometry.adjusted(-h_padding, -v_padding, h_padding, v_padding)
        height = padded_geometry.height()
        radius = height // 2

        # Apply Style
        self.anim_pill.setStyleSheet(f"""
            #anim_pill {{
                background-color: #0f0f12; 
                border-radius: {radius}px; 
                border: 1px solid #333333;
            }}
        """)

        if immediate:
            self.anim_pill.setGeometry(padded_geometry)
            self.anim_pill.show()
        else:
            if self.nav_animation.state() == QPropertyAnimation.Running:
                self.nav_animation.stop()

            self.nav_animation.setStartValue(self.anim_pill.geometry())
            self.nav_animation.setEndValue(padded_geometry)
            self.nav_animation.start()

    def setup_quality_buttons(self):
        if hasattr(self.ui, 'btnQualBest'):
             self.ui.btnQualBest.clicked.connect(self.set_quality_best)
             self.ui.btnQualBest.setChecked(True)

        if hasattr(self.ui, 'comboQuality'):
            self.ui.comboQuality.clear()
            items = [
                "4k (2160p)", 
                "1440p (2K)", 
                "1080p (HD)", 
                "720p", 
                "480p", 
                "360p", 
                "144p"
            ]
            self.ui.comboQuality.addItems(items)
            
            # Connect signal
            self.ui.comboQuality.currentIndexChanged.connect(self.handle_quality_combo)

    def set_quality_best(self):
        """Reset to Best Available"""
        self.current_quality = None
        print("Quality: Best Available")
        
        # Reset Dropdown visual
        if hasattr(self.ui, 'comboQuality'):
            self.ui.comboQuality.setCurrentIndex(-1) 

        # Update Label
        if hasattr(self, 'lbl_quality_badge'):
            self.lbl_quality_badge.setText("Best Quality Available")

    def handle_quality_combo(self, index):
        """Parse dropdown text to get integer quality AND update UI immediately"""
        text = self.ui.comboQuality.currentText()

        if hasattr(self.ui, 'btnQualBest'):
            self.ui.btnQualBest.setChecked(False)

        # Logic to determine quality value
        if "2160" in text: self.current_quality = 2160
        elif "1440" in text: self.current_quality = 1440
        elif "1080" in text: self.current_quality = 1080
        elif "720" in text: self.current_quality = 720
        elif "480" in text: self.current_quality = 480
        elif "360" in text: self.current_quality = 360
        elif "144" in text: self.current_quality = 144
        else: self.current_quality = None # Default/Fallback
        
        print(f"Quality set to: {self.current_quality}p")

        # Update the Metadata Card Label Real-Time
        if hasattr(self, 'lbl_quality_badge'):
            if self.current_quality is None:
                new_text = "Best Quality Available"
            else:
                new_text = f"{self.current_quality}p Selected"
            
            self.lbl_quality_badge.setText(new_text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker-spotdl":
        try:
            if sys.platform == 'win32':
                original_popen = subprocess.Popen
                
                class HiddenPopen(original_popen):
                    def __init__(self, *args, **kwargs):
                        if 'creationflags' not in kwargs:
                            kwargs['creationflags'] = 0x08000000
                        else:
                            kwargs['creationflags'] |= 0x08000000
                        super().__init__(*args, **kwargs)
                
                subprocess.Popen = HiddenPopen

            sys.argv.pop(1)      
            sys.argv[0] = "spotdl" 
            
            from spotdl.console.entry_point import console_entry_point
            console_entry_point()
            
        except Exception as e:
            print(f"[ERROR] Worker failed: {e}")
        
        sys.exit()
    myappid = 'vac.v1' 
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    manrope_path = os.path.join(base_dir, "fonts", "manrope", "Manrope-VariableFont_wght.ttf")
    if os.path.exists(manrope_path):
        QFontDatabase.addApplicationFont(manrope_path)

    jetbrains_path = os.path.join(base_dir, "fonts", "JetBrains_Mono", "JetBrainsMono-VariableFont_wght.ttf")
    if os.path.exists(jetbrains_path):
        QFontDatabase.addApplicationFont(jetbrains_path)

    font_id = QFontDatabase.addApplicationFont(manrope_path)
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            app.setFont(QFont(families[0], 10))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())