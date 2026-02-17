import sys
import os
import subprocess
import shutil
import gettext
import yt_dlp
import re 

def shim_translation(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=None):
    return gettext.NullTranslations()

gettext.translation = shim_translation

FFMPEG_EXE_PATH = None

def get_download_path():
    return os.path.join('C:\\', 'VAC Downloads')

def check_ffmpeg():
    global FFMPEG_EXE_PATH
    # If already set, skip check
    if FFMPEG_EXE_PATH: return True

    if hasattr(sys, '_MEIPASS'):
        bundled_path = os.path.join(sys._MEIPASS, 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(bundled_path):
            FFMPEG_EXE_PATH = bundled_path
            print(f"FFmpeg detected (Bundled): {FFMPEG_EXE_PATH}")
            return True

    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(base_dir, 'ffmpeg', 'ffmpeg.exe')
    if os.path.exists(local_path):
        FFMPEG_EXE_PATH = local_path
        print(f"FFmpeg detected (Local Folder): {FFMPEG_EXE_PATH}")
        return True

    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        FFMPEG_EXE_PATH = ffmpeg_path
        print("FFmpeg detected (System PATH).")
        return True
    
    print("ALERT: FFmpeg NOT detected.")
    return False

def get_file_metadata(file_path):
    """
    Uses FFmpeg to get the real duration and extract the embedded cover art.
    Returns (duration_string, thumbnail_path)
    """
    check_ffmpeg()
    duration = "--:--"
    thumb_path = "None"
    
    if not os.path.exists(file_path) or not FFMPEG_EXE_PATH:
        return duration, thumb_path

    # Get Duration
    try:
        # ffmpeg -i file.mp3 ... outputs info to stderr
        cmd = [FFMPEG_EXE_PATH, '-i', file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        
        match = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2})", result.stderr)
        if match:
            h, m, s = match.groups()
            if h == "00":
                duration = f"{int(m):02d}:{int(s):02d}"
            else:
                duration = f"{int(h)}:{int(m):02d}:{int(s):02d}"
    except Exception as e:
        print(f"Error reading duration: {e}")

    # Extract Embedded Thumbnail
    try:
        # Create thumbnails folder
        base_dir = get_download_path()
        thumb_dir = os.path.join(base_dir, 'thumbnails')
        if not os.path.exists(thumb_dir):
            os.makedirs(thumb_dir)
            
        # Use filename as unique ID
        name = os.path.splitext(os.path.basename(file_path))[0]
        out_thumb = os.path.join(thumb_dir, f"{name}.jpg")
        
        # ffmpeg -i file.mp3 -an -vcodec copy out.jpg -y
        # -an: no audio, -vcodec copy: extract image as-is
        cmd_thumb = [FFMPEG_EXE_PATH, '-i', file_path, '-an', '-vcodec', 'copy', out_thumb, '-y']
        subprocess.run(cmd_thumb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        
        if os.path.exists(out_thumb):
            thumb_path = out_thumb
            
    except Exception as e:
        print(f"Error extracting thumbnail: {e}")
        
    return duration, thumb_path

def find_best_match_file(folder, name_hint):
    """
    Scans the folder for the file that best matches the name_hint.
    """
    try:
        if not os.path.exists(folder):
            return None

        def get_tokens(text):
            return set(part for part in re.split(r'\W+', text.lower()) if part)

        hint_tokens = get_tokens(name_hint)
        if not hint_tokens: return None

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        
        best_file = None
        best_score = 0.0      
        best_jaccard = 0.0    

        for f in files:
            f_name_only = os.path.splitext(f)[0]
            file_tokens = get_tokens(f_name_only)
            
            common_tokens = hint_tokens.intersection(file_tokens)
            if not common_tokens: continue

            coverage_score = len(common_tokens) / len(hint_tokens)
            
            union_len = len(hint_tokens.union(file_tokens))
            jaccard_score = len(common_tokens) / union_len if union_len > 0 else 0

            if coverage_score > best_score:
                best_score = coverage_score
                best_jaccard = jaccard_score
                best_file = f
            elif coverage_score == best_score:
                if jaccard_score > best_jaccard:
                    best_jaccard = jaccard_score
                    best_file = f
        
        if best_file and best_score >= 0.8:
            return os.path.join(folder, best_file)
            
    except Exception as e:
        print(f"Error searching for file: {e}")
    
    return None

def download_with_spotdl(url):
    """
    Uses the SpotDL CLI with clean error handling for private playlists.
    """
    check_ffmpeg() # Ensure FFMPEG is ready
    
    base_folder = get_download_path()
    output_dir = os.path.join(base_folder, 'mp3')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_template = os.path.join(output_dir, "{title} - {artist}.{output-ext}")
    print(f"Launching SpotDL CLI for: {url}")

    if getattr(sys, 'frozen', False):
        cmd = [
            sys.executable, 
            "--worker-spotdl", 
            url, 
            "--output", output_template,
            "--simple-tui",
            "--search-query", "{artist} - {title}",
            "--dont-filter-results",
            "--threads", "8",
            "--preload",
            "--bitrate", "320k"
        ]
    else:
        cmd = [
            sys.executable, "-m", "spotdl", 
            url, 
            "--output", output_template,
            "--simple-tui",
            "--search-query", "{artist} - {title}", 
            "--dont-filter-results",
            "--threads", "8",
            "--preload",
            "--bitrate", "320k"
        ]

    if FFMPEG_EXE_PATH:
        cmd.extend(["--ffmpeg", FFMPEG_EXE_PATH])

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding='utf-8', errors='replace', env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )

        suppress_traceback = False 

        for line in process.stdout:
            clean_line = line.strip()
            if not clean_line: continue

            if "Traceback" in clean_line or "ResponseError" in clean_line:
                suppress_traceback = True
            
            if "too many 404 error responses" in clean_line:
                suppress_traceback = True 
                continue

            if suppress_traceback: continue

            print(f"[CLI] {clean_line}")

            if "Downloaded" in clean_line and '"' in clean_line:
                try:
                    parts = clean_line.split('"')
                    if len(parts) > 1:
                        song_hint = parts[1]
                        actual_path = find_best_match_file(output_dir, song_hint)
                        
                        if actual_path:
                            real_duration, real_thumb = get_file_metadata(actual_path)
                            print(f"[HISTORY_LOG] {song_hint}::VAC::MP3::VAC::{actual_path}::VAC::{real_duration}::VAC::{real_thumb}", flush=True)
                        else:
                            print(f"[SYSTEM] Could not resolve file path for: {song_hint}")
                except:
                    pass

        process.wait()
        
    except Exception as e:
        print(f"Error running SpotDL CLI: {e}")

class YtdlLogger:
    def debug(self, msg):
        if msg.startswith('[download] Destination:'):
            print(msg)
        elif "Extracting URL" in msg:
            print("Fetching video metadata...")
    def info(self, msg): pass 
    def warning(self, msg): pass
    def error(self, msg): 
        if "Private video" in msg:
            print(f"Skipping private/deleted video...")
        else:
            print(f"Error: {msg}")

def download_media(url_or_search_term, mode='video', max_height=None, search_query=None):
    check_ffmpeg() # Ensure FFMPEG is ready
    
    is_search = search_query is not None
    base_folder = get_download_path()
    sub_folder = 'mp3' if mode == 'audio' or is_search else 'mp4'
    final_path = os.path.join(base_folder, sub_folder)

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    if mode == 'audio' or is_search:
        fmt_label = "MP3"
    else:
        fmt_label = "MP4"

    def internal_progress_hook(d):
        if d['status'] == 'downloading':
            p = 0
            if 'total_bytes' in d:
                p = d['downloaded_bytes'] / d['total_bytes'] * 100
            elif 'total_bytes_estimate' in d:
                p = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
            print(f"[PROGRESS] {int(p)}")

    def internal_post_hook(d):
        if d['status'] == 'finished':
            try:
                info = d.get('info_dict', {})
                final_filename = info.get('filepath') or info.get('filename')
                
                # Filter extensions
                if final_filename:
                    ext = os.path.splitext(final_filename)[1].lower()
                    if (mode == 'audio' or is_search) and ext != '.mp3': return
                    if mode == 'video' and ext != '.mp4': return

                title = info.get('title')
                
                # Get Duration
                duration = info.get('duration_string', '--:--')
                if ':' not in duration: duration = f"0:{duration}"

                # Find Thumbnail File
                # yt-dlp saves thumbnails with the same basename but different extension
                thumb_path = "None"
                if final_filename:
                    base_name = os.path.splitext(final_filename)[0]
                    # Check common thumbnail extensions
                    for ext in ['.webp', '.jpg', '.png', '.jpeg']:
                        potential_thumb = base_name + ext
                        if os.path.exists(potential_thumb):
                            thumb_path = potential_thumb
                            break

                if final_filename and os.path.exists(final_filename):
                    print(f"[HISTORY_LOG] {title}::VAC::{fmt_label}::VAC::{final_filename}::VAC::{duration}::VAC::{thumb_path}", flush=True)

            except Exception as e:
                print(f"Error in post-hook: {e}")

    ydl_opts = {
        'outtmpl': f'{final_path}/%(title)s.%(ext)s', 
        'restrictfilenames': True,
        'progress_hooks': [internal_progress_hook], 
        'postprocessor_hooks': [internal_post_hook],
        'logger': YtdlLogger(),
        'quiet': True,
        'no_warnings': True,
        'overwrites': True,
        'ignoreerrors': True,
        'writethumbnail': True,
        'cookiesfrombrowser': ('chrome',), 
    }
    
    if FFMPEG_EXE_PATH:
        ydl_opts['ffmpeg_location'] = FFMPEG_EXE_PATH

    print("Initializing yt-dlp subprocess...")

    if mode == 'audio' or is_search:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', 
        }]
        target = search_query if is_search else url_or_search_term
    else:
        video_fmt = f"[height<={max_height}]" if max_height else ""
        ydl_opts['format'] = f'bestvideo{video_fmt}[ext=mp4]+bestaudio[ext=m4a]/best{video_fmt}[ext=mp4]/best{video_fmt}'
        target = url_or_search_term

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target, download=False)
            if 'title' in info and 'entries' not in info:
                print(f"[METADATA] {info['title']}")
            elif 'title' in info:
                print(f"[METADATA] Playlist: {info['title']}")
            
            ydl.download([target])
            print(f"Saved to: {final_path}")
    except Exception as e:
        print(f"Download Error: {e}")