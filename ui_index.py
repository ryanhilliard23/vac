# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)
import resources_rc
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1298, 709)
        MainWindow.setMinimumSize(QSize(1298, 709))
        MainWindow.setMaximumSize(QSize(1298, 709))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: #0f0f10;")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sidebar_2 = QWidget(self.centralwidget)
        self.sidebar_2.setObjectName(u"sidebar_2")
        font = QFont()
        font.setFamilies([u"Manrope SemiBold"])
        self.sidebar_2.setFont(font)
        self.sidebar_2.setStyleSheet(u"background-color: rgb(15, 15, 16);")
        self.stackedWidget = QStackedWidget(self.sidebar_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 100, 1301, 611))
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet(u"background-color: transparent;")
        self.download_page = QWidget()
        self.download_page.setObjectName(u"download_page")
        self.download_page.setStyleSheet(u"background-color: #0f0f10;")
        self.inputContainer = QFrame(self.download_page)
        self.inputContainer.setObjectName(u"inputContainer")
        self.inputContainer.setGeometry(QRect(190, 10, 941, 80))
        self.inputContainer.setMinimumSize(QSize(80, 80))
        self.inputContainer.setStyleSheet(u"/* 1. THE CONTAINER (The visual \"Card\") */\n"
"QFrame#inputContainer {\n"
"    /* Dark glass-like background */\n"
"    background-color: #1c1c1e; \n"
"    /* Subtle border */\n"
"    border: 1px solid rgba(255, 255, 255, .08); \n"
"    /* Rounded corners */\n"
"    border-radius: 12px; \n"
"}\n"
"\n"
"/* Hover Effect: The Blue Glow */\n"
"QFrame#inputContainer:hover {\n"
"    border: 2px solid rgb(59, 130, 246); /* Blue-ish border */\n"
"    background-color: rgb(30, 30, 35);\n"
"}\n"
"\n"
"/* 2. THE INPUT FIELD (The \"Invisible\" Text Layer) */\n"
"QLineEdit#urlInput {\n"
"    /* CRITICAL: Removes the \"box\" look */\n"
"    background: transparent; \n"
"    border: none; \n"
"    \n"
"    /* Typography */\n"
"    color: #E5E7EB; /* Gray-200 */\n"
"    font-family: 'Manrope';\n"
"    font-size: 14px;\n"
"    font-weight: 500;\n"
"    \n"
"    /* Spacing inside the text area */\n"
"    padding: 14px 10px; \n"
"}\n"
"\n"
"/* 3. THE PASTE BUTTON (Integrated Pill) */\n"
"QPushButton#pasteBtn {\n"
"    backgrou"
                        "nd-color: #1F1F23;\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);\n"
"    border-radius: 6px;\n"
"    color: #9CA3AF; /* Gray-400 */\n"
"    font-weight: bold;\n"
"    font-size: 10px;\n"
"    \n"
"    /* Sizing */\n"
"    min-width: 60px;\n"
"    height: 24px;\n"
"    \n"
"    /* Position it away from the edges */\n"
"    margin-right: 12px;\n"
"    margin-left: 5px;\n"
"}\n"
"\n"
"/* Button Hover */\n"
"QPushButton#pasteBtn:hover {\n"
"    background-color: #3B82F6; /* Primary Blue */\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"/* 4. THE ICON (Link Symbol) */\n"
"QLabel#iconLabel {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #6B7280; /* Gray-500 */\n"
"    \n"
"    /* Spacing from left edge */\n"
"    padding-left: 15px;\n"
"    padding-right: 5px;\n"
"    \n"
"    /* Size */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.inputContainer.setFrameShape(QFrame.StyledPanel)
        self.inputContainer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.inputContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.iconLabel = QLabel(self.inputContainer)
        self.iconLabel.setObjectName(u"iconLabel")
        font1 = QFont()
        font1.setFamilies([u"Manrope SemiBold"])
        font1.setPointSize(12)
        self.iconLabel.setFont(font1)
        self.iconLabel.setStyleSheet(u"background-color: transparent;\n"
"color: white;")
        self.iconLabel.setPixmap(QPixmap(u":/images/link-simple.png"))
        self.iconLabel.setScaledContents(False)

        self.horizontalLayout_2.addWidget(self.iconLabel)

        self.urlInput = QLineEdit(self.inputContainer)
        self.urlInput.setObjectName(u"urlInput")
        font2 = QFont()
        font2.setFamilies([u"Manrope"])
        font2.setBold(False)
        font2.setItalic(False)
        self.urlInput.setFont(font2)
        self.urlInput.setStyleSheet(u"font: 18px;")

        self.horizontalLayout_2.addWidget(self.urlInput)

        self.pasteBtn = QPushButton(self.inputContainer)
        self.pasteBtn.setObjectName(u"pasteBtn")
        font3 = QFont()
        font3.setBold(True)
        self.pasteBtn.setFont(font3)
        self.pasteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pasteBtn.setStyleSheet(u"background-color: #2c2c2e;\n"
"border-radius: 7px;\n"
"color: white;\n"
"")
        self.pasteBtn.setIconSize(QSize(16, 16))
        self.pasteBtn.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.pasteBtn)

        self.btnAddQueue = QPushButton(self.inputContainer)
        self.btnAddQueue.setObjectName(u"btnAddQueue")
        font4 = QFont()
        font4.setFamilies([u"Inter"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.btnAddQueue.setFont(font4)
        self.btnAddQueue.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnAddQueue.setFocusPolicy(Qt.StrongFocus)
        self.btnAddQueue.setStyleSheet(u"background-color: rgb(54, 123, 239);\n"
"border-radius: 7px;\n"
"\n"
"")
        icon = QIcon()
        icon.addFile(u":/images/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddQueue.setIcon(icon)
        self.btnAddQueue.setIconSize(QSize(25, 25))
        self.btnAddQueue.setCheckable(True)
        self.btnAddQueue.setFlat(False)

        self.horizontalLayout_2.addWidget(self.btnAddQueue)

        self.metadata_placeholder = QFrame(self.download_page)
        self.metadata_placeholder.setObjectName(u"metadata_placeholder")
        self.metadata_placeholder.setGeometry(QRect(190, 100, 941, 1))
        self.metadata_placeholder.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.metadata_placeholder.setFrameShape(QFrame.NoFrame)
        self.metadata_placeholder.setFrameShadow(QFrame.Raised)
        self.main_frame = QFrame(self.download_page)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setGeometry(QRect(180, 100, 961, 421))
        self.main_frame.setStyleSheet(u"background-color: transparent;\n"
"outline: none;\n"
"border: none;")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.main_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.main_container = QFrame(self.main_frame)
        self.main_container.setObjectName(u"main_container")
        self.main_container.setStyleSheet(u"background-color: transparent;\n"
"outline: none;\n"
"border: none;")
        self.main_container.setFrameShape(QFrame.StyledPanel)
        self.main_container.setFrameShadow(QFrame.Raised)
        self.option_container = QFrame(self.main_container)
        self.option_container.setObjectName(u"option_container")
        self.option_container.setGeometry(QRect(0, 0, 661, 225))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_container.sizePolicy().hasHeightForWidth())
        self.option_container.setSizePolicy(sizePolicy)
        self.option_container.setStyleSheet(u"#option_container {\n"
"    background-color: transparent; /* Keep trying to be transparent */\n"
"    border-bottom-left-radius: 15px; /* Match the parent's radius */\n"
"    border-bottom-right-radius: 15px; /* Match the parent's radius */\n"
"}")
        self.option_container.setFrameShape(QFrame.StyledPanel)
        self.option_container.setFrameShadow(QFrame.Raised)
        self.format_qual_frame = QFrame(self.option_container)
        self.format_qual_frame.setObjectName(u"format_qual_frame")
        self.format_qual_frame.setGeometry(QRect(0, 10, 641, 191))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.format_qual_frame.sizePolicy().hasHeightForWidth())
        self.format_qual_frame.setSizePolicy(sizePolicy1)
        self.format_qual_frame.setMinimumSize(QSize(318, 179))
        self.format_qual_frame.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame.setFrameShadow(QFrame.Raised)
        self.btnFormatVideo = QPushButton(self.format_qual_frame)
        self.btnFormatVideo.setObjectName(u"btnFormatVideo")
        self.btnFormatVideo.setGeometry(QRect(15, 70, 132, 112))
        font5 = QFont()
        font5.setFamilies([u"Manrope,sans-serif"])
        font5.setBold(True)
        self.btnFormatVideo.setFont(font5)
        self.btnFormatVideo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnFormatVideo.setLayoutDirection(Qt.LeftToRight)
        self.btnFormatVideo.setStyleSheet(u"/* --- Video & Audio Toggle Buttons --- */\n"
"QPushButton#btnFormatVideo, QPushButton#btnFormatAudio {\n"
"    background-color: #0F0F12;        /* matches bg-surface */\n"
"    border: 1px solid #2A2A30;        /* matches border-white/5 */\n"
"    border-radius: 12px;              /* matches rounded-xl */\n"
"    color: #9ca3af;                   /* matches text-gray-400 */\n"
"    font-family: \"Manrope\", sans-serif;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    text-align: left;\n"
"    padding: 15px;                    /* spacious padding like the card */\n"
"    qproperty-iconSize: 24px 24px;    /* makes the icon larger (text-2xl) */\n"
"}\n"
"\n"
"/* --- Hover State --- */\n"
"QPushButton#btnFormatVideo:hover, QPushButton#btnFormatAudio:hover {\n"
"    background-color: #1A1A1F;        /* matches hover:bg-white/5 */\n"
"    border: 1px solid #3f3f46;        /* slightly lighter border */\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* --- Active / Checked State (The Blue Look) --- */\n"
"/* This"
                        " mimics the \"Video\" active state in your HTML */\n"
"QPushButton#btnFormatVideo:checked, QPushButton#btnFormatAudio:checked {\n"
"    background-color: rgba(59, 130, 246, 0.15); /* Blue tint (bg-primary/10) */\n"
"    border: 1px solid rgba(59, 130, 246, 0.5);  /* Blue border (border-primary/50) */\n"
"    color: #ffffff;                             /* White text */\n"
"}")
        self.btnFormatVideo.setCheckable(True)
        self.btnFormatVideo.setChecked(False)
        self.btnFormatAudio = QPushButton(self.format_qual_frame)
        self.btnFormatAudio.setObjectName(u"btnFormatAudio")
        self.btnFormatAudio.setGeometry(QRect(165, 70, 132, 112))
        self.btnFormatAudio.setFont(font5)
        self.btnFormatAudio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnFormatAudio.setStyleSheet(u"/* --- Video & Audio Toggle Buttons --- */\n"
"QPushButton#btnFormatVideo, QPushButton#btnFormatAudio {\n"
"    background-color: #0F0F12;        /* matches bg-surface */\n"
"    border: 1px solid #2A2A30;        /* matches border-white/5 */\n"
"    border-radius: 12px;              /* matches rounded-xl */\n"
"    color: #9ca3af;                   /* matches text-gray-400 */\n"
"    font-family: \"Manrope\", sans-serif;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    text-align: left;\n"
"    padding: 15px;                    /* spacious padding like the card */\n"
"    qproperty-iconSize: 24px 24px;    /* makes the icon larger (text-2xl) */\n"
"}\n"
"\n"
"/* --- Hover State --- */\n"
"QPushButton#btnFormatVideo:hover, QPushButton#btnFormatAudio:hover {\n"
"    background-color: #1A1A1F;        /* matches hover:bg-white/5 */\n"
"    border: 1px solid #3f3f46;        /* slightly lighter border */\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* --- Active / Checked State (The Blue Look) --- */\n"
"/* This"
                        " mimics the \"Video\" active state in your HTML */\n"
"QPushButton#btnFormatVideo:checked, QPushButton#btnFormatAudio:checked {\n"
"    background-color: rgba(59, 130, 246, 0.15); /* Blue tint (bg-primary/10) */\n"
"    border: 1px solid rgba(59, 130, 246, 0.5);  /* Blue border (border-primary/50) */\n"
"    color: #ffffff;                             /* White text */\n"
"}")
        self.btnFormatAudio.setCheckable(True)
        self.logo_text_3 = QLabel(self.format_qual_frame)
        self.logo_text_3.setObjectName(u"logo_text_3")
        self.logo_text_3.setGeometry(QRect(20, 40, 101, 31))
        font6 = QFont()
        font6.setFamilies([u"Manrope SemiBold"])
        font6.setPointSize(10)
        self.logo_text_3.setFont(font6)
        self.logo_text_3.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.mp3_icon = QLabel(self.format_qual_frame)
        self.mp3_icon.setObjectName(u"mp3_icon")
        self.mp3_icon.setGeometry(QRect(180, 90, 21, 21))
        self.mp3_icon.setFont(font1)
        self.mp3_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp3_icon.setPixmap(QPixmap(u":/images/waveform-active.png"))
        self.mp3_icon.setScaledContents(True)
        self.mp4_icon = QLabel(self.format_qual_frame)
        self.mp4_icon.setObjectName(u"mp4_icon")
        self.mp4_icon.setGeometry(QRect(30, 90, 21, 21))
        self.mp4_icon.setFont(font1)
        self.mp4_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon.setPixmap(QPixmap(u":/images/film-active.png"))
        self.mp4_icon.setScaledContents(True)
        self.logo_text_7 = QLabel(self.format_qual_frame)
        self.logo_text_7.setObjectName(u"logo_text_7")
        self.logo_text_7.setGeometry(QRect(32, 133, 21, 31))
        font7 = QFont()
        font7.setFamilies([u"JetBrains Mono"])
        font7.setPointSize(8)
        self.logo_text_7.setFont(font7)
        self.logo_text_7.setStyleSheet(u"background-color: transparent;\n"
"color: #4B5563;\n"
"border: none;")
        self.logo_text_8 = QLabel(self.format_qual_frame)
        self.logo_text_8.setObjectName(u"logo_text_8")
        self.logo_text_8.setGeometry(QRect(180, 130, 21, 31))
        self.logo_text_8.setFont(font7)
        self.logo_text_8.setStyleSheet(u"background-color: transparent;\n"
"color: #4B5563;\n"
"border: none;")
        self.logo_text_6 = QLabel(self.format_qual_frame)
        self.logo_text_6.setObjectName(u"logo_text_6")
        self.logo_text_6.setGeometry(QRect(330, 40, 101, 31))
        self.logo_text_6.setFont(font6)
        self.logo_text_6.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"outline: none;\n"
"border: none;")
        self.comboQuality = QComboBox(self.format_qual_frame)
        self.comboQuality.addItem("")
        self.comboQuality.setObjectName(u"comboQuality")
        self.comboQuality.setGeometry(QRect(330, 70, 281, 51))
        self.comboQuality.setFont(font5)
        self.comboQuality.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.comboQuality.setStyleSheet(u"/* --- QComboBox Base Style --- */\n"
"QComboBox {\n"
"    background-color: #0F0F12;      /* matches bg-surface */\n"
"    border: 1px solid #2A2A30;      /* matches border-white/5 */\n"
"    border-radius: 12px;            /* matches rounded-xl */\n"
"    padding: 10px 16px;             /* matches py-3 px-4 */\n"
"    color: #9ca3af;                 /* matches text-gray-400 */\n"
"    font-family: \"Manrope\", sans-serif;\n"
"    font-size: 13px;                /* matches text-sm */\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"/* --- Hover State --- */\n"
"QComboBox:hover {\n"
"    background-color: #1A1A1F;      /* matches hover:bg-surfaceHighlight */\n"
"    color: #ffffff;                 /* lighter text on hover */\n"
"    border: 1px solid #3f3f46;\n"
"}\n"
"\n"
"/* --- Focus / Open State --- */\n"
"QComboBox:on { \n"
"    border: 1px solid rgba(59, 130, 246, 0.5); /* matches focus:border-primary/50 */\n"
"    background-color: #0F0F12;\n"
"}\n"
"\n"
"/* --- The Dropdown Button Area --- */\n"
"QComboBox::dr"
                        "op-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 40px; \n"
"    border-left-width: 0px;\n"
"    border-top-right-radius: 12px;\n"
"    border-bottom-right-radius: 12px;\n"
"    background: transparent;        /* Keep transparent to show parent bg */\n"
"}\n"
"\n"
"/* --- The Arrow Icon --- */\n"
"/* Note: You need a PNG icon in your resource file for this to look perfect.\n"
"   If you don't have one, Qt uses a default Windows arrow. */\n"
"QComboBox::down-arrow {\n"
"    image: url(:/images/caret-down.png); /* Replace with your actual resource path */\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    padding-right: 16px; /* Offset to match the HTML look */\n"
"}\n"
"\n"
"/* --- The Popup List (The part that opens up) --- */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #0F0F12;      /* Dark background */\n"
"    border: 1px solid #2A2A30;      /* Thin border */\n"
"    selection-background-color: #1A1A1F; /* Hovered Item Background */\n"
"    "
                        "selection-color: #ffffff;       /* Hovered Item Text */\n"
"    outline: 0px;                   /* Remove dotted selection line */\n"
"    padding: 4px;\n"
"    border-radius: 8px;\n"
"    color: #9ca3af;\n"
"}")
        self.logo_text_10 = QLabel(self.format_qual_frame)
        self.logo_text_10.setObjectName(u"logo_text_10")
        self.logo_text_10.setGeometry(QRect(50, 13, 231, 21))
        font8 = QFont()
        font8.setFamilies([u"Manrope SemiBold"])
        font8.setPointSize(11)
        self.logo_text_10.setFont(font8)
        self.logo_text_10.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_3 = QLabel(self.format_qual_frame)
        self.mp4_icon_3.setObjectName(u"mp4_icon_3")
        self.mp4_icon_3.setGeometry(QRect(20, 13, 21, 21))
        self.mp4_icon_3.setFont(font1)
        self.mp4_icon_3.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_3.setPixmap(QPixmap(u":/images/control.png"))
        self.mp4_icon_3.setScaledContents(True)
        self.sys_prog_container = QFrame(self.main_container)
        self.sys_prog_container.setObjectName(u"sys_prog_container")
        self.sys_prog_container.setGeometry(QRect(0, 210, 661, 191))
        self.sys_prog_container.setStyleSheet(u"background-color: transparent;")
        self.sys_prog_container.setFrameShape(QFrame.StyledPanel)
        self.sys_prog_container.setFrameShadow(QFrame.Raised)
        self.log_container = QFrame(self.sys_prog_container)
        self.log_container.setObjectName(u"log_container")
        self.log_container.setGeometry(QRect(0, 30, 641, 161))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.log_container.sizePolicy().hasHeightForWidth())
        self.log_container.setSizePolicy(sizePolicy2)
        self.log_container.setMinimumSize(QSize(600, 150))
        self.log_container.setStyleSheet(u"background-color: transparent;")
        self.log_container.setFrameShape(QFrame.StyledPanel)
        self.log_container.setFrameShadow(QFrame.Raised)
        self.consoleLog = QTextEdit(self.log_container)
        self.consoleLog.setObjectName(u"consoleLog")
        self.consoleLog.setGeometry(QRect(0, 10, 641, 151))
        font9 = QFont()
        font9.setFamilies([u"Consolas,Monaco,Courier New,monospace"])
        font9.setPointSize(10)
        self.consoleLog.setFont(font9)
        self.consoleLog.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.consoleLog.setStyleSheet(u"/* 1. MAIN TEXT AREA STYLE */\n"
"QTextEdit, QPlainTextEdit {\n"
"    background-color: #1c1c1e;\n"
"    border: 1px solid #2c2c2e; \n"
"    \n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"\n"
"    padding: 10px;\n"
"    color: #c8c8c8;\n"
"    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"/* 2. NEW SCROLLBAR STYLE (Matches History Table) */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #0f0f12;\n"
"    width: 14px;\n"
"    margin: 15px 4px 15px 4px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #2A2A30;\n"
"    min-height: 30px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #3f3f46;\n"
"}\n"
"QScrollBar::add-line:vertical, \n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
""
                        "    background: none;\n"
"}\n"
"")
        self.consoleLog.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.consoleLog.setReadOnly(True)
        self.frame_3 = QFrame(self.sys_prog_container)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 10, 641, 31))
        self.frame_3.setStyleSheet(u"background-color: rgb(15, 15, 18);\n"
"border: 1px solid #2c2c2e;\n"
"\n"
"/* Curve only the top */\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"\n"
"/* Bottom stays straight */\n"
"border-bottom-left-radius: 0;\n"
"border-bottom-right-radius: 0;\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.logo_text_9 = QLabel(self.frame_3)
        self.logo_text_9.setObjectName(u"logo_text_9")
        self.logo_text_9.setGeometry(QRect(30, 0, 111, 31))
        self.logo_text_9.setFont(font7)
        self.logo_text_9.setStyleSheet(u"background-color: transparent;\n"
"color: #4B5563;\n"
"border: none;")
        self.mp3_icon_2 = QLabel(self.frame_3)
        self.mp3_icon_2.setObjectName(u"mp3_icon_2")
        self.mp3_icon_2.setGeometry(QRect(6, 7, 19, 19))
        self.mp3_icon_2.setFont(font1)
        self.mp3_icon_2.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp3_icon_2.setPixmap(QPixmap(u":/images/terminal-window-fill.png"))
        self.mp3_icon_2.setScaledContents(True)
        self.download_container = QFrame(self.main_container)
        self.download_container.setObjectName(u"download_container")
        self.download_container.setGeometry(QRect(660, 0, 281, 401))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.download_container.sizePolicy().hasHeightForWidth())
        self.download_container.setSizePolicy(sizePolicy3)
        self.download_container.setMinimumSize(QSize(261, 401))
        self.download_container.setStyleSheet(u"background-color: transparent;\n"
"outline: none;\n"
"border: none;")
        self.download_container.setFrameShape(QFrame.StyledPanel)
        self.download_container.setFrameShadow(QFrame.Raised)
        self.frame_4 = QFrame(self.download_container)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(0, 10, 281, 291))
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy4)
        self.frame_4.setMinimumSize(QSize(250, 179))
        self.frame_4.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.queue_table = QTableWidget(self.frame_4)
        self.queue_table.setObjectName(u"queue_table")
        self.queue_table.setGeometry(QRect(0, 40, 281, 251))
        self.queue_table.setStyleSheet(u"border-top-left-radius: 0px;\n"
"border-top-right-radius: 0px;\n"
"border-bottom-left-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"border: none;\n"
"outline: none;\n"
"background-color: transparent;")
        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(0, 0, 281, 41))
        self.frame_5.setStyleSheet(u"background-color: rgb(15, 15, 18);\n"
"border: 1px solid #2c2c2e;\n"
"\n"
"/* Curve only the top */\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"\n"
"/* Bottom stays straight */\n"
"border-bottom-left-radius: 0;\n"
"border-bottom-right-radius: 0;\n"
"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.download_queue = QLabel(self.frame_5)
        self.download_queue.setObjectName(u"download_queue")
        self.download_queue.setGeometry(QRect(10, 10, 191, 21))
        font10 = QFont()
        font10.setFamilies([u"Manrope"])
        font10.setPointSize(10)
        self.download_queue.setFont(font10)
        self.download_queue.setStyleSheet(u"background-color: transparent;\n"
"color: #d1d5db;\n"
"border: none;")
        self.btnClearQueue = QPushButton(self.frame_5)
        self.btnClearQueue.setObjectName(u"btnClearQueue")
        self.btnClearQueue.setGeometry(QRect(248, 5, 31, 31))
        self.btnClearQueue.setFont(font3)
        self.btnClearQueue.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnClearQueue.setStyleSheet(u"border: none;\n"
"color: #3879e4;\n"
"background-color: transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/images/trash-wh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnClearQueue.setIcon(icon1)
        self.btnClearQueue.setCheckable(True)
        self.btnStartDownload = QPushButton(self.download_container)
        self.btnStartDownload.setObjectName(u"btnStartDownload")
        self.btnStartDownload.setGeometry(QRect(0, 320, 281, 81))
        sizePolicy1.setHeightForWidth(self.btnStartDownload.sizePolicy().hasHeightForWidth())
        self.btnStartDownload.setSizePolicy(sizePolicy1)
        self.btnStartDownload.setMinimumSize(QSize(0, 0))
        self.btnStartDownload.setFont(font5)
        self.btnStartDownload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnStartDownload.setStyleSheet(u"/* --- Main Download Button (Gradient Style) --- */\n"
"QPushButton#btnStartDownload {\n"
"    /* Gradient Background: Matches 'bg-gradient-to-b from-primary to-blue-700' */\n"
"    background-color: qlineargradient(\n"
"        spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, \n"
"        stop:0 #3B82F6, \n"
"        stop:1 #1d4ed8\n"
"    );\n"
"    \n"
"    /* Border & Radius */\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);\n"
"    border-radius: 16px;  /* Matches 'rounded-2xl' */\n"
"    \n"
"    /* Text Styling */\n"
"    color: white;\n"
"    font-family: \"Manrope\", sans-serif;\n"
"    font-size: 18px;      /* Large text like the HTML <h2> */\n"
"    font-weight: bold;\n"
"    text-align: left;\n"
"    /* Spacing */\n"
"    padding: 20px;        /* Large padding to mimic the card size */\n"
"}\n"
"\n"
"/* --- Hover State --- */\n"
"QPushButton#btnStartDownload:hover {\n"
"    /* Slightly lighter gradient to mimic the scale/glow effect */\n"
"    background-color: qlineargradient(\n"
"        spread:pad, x"
                        "1:0.5, y1:0, x2:0.5, y2:1, \n"
"        stop:0 #60a5fa,   /* Lighter Blue */\n"
"        stop:1 #2563eb    /* Blue-600 */\n"
"    );\n"
"    border: 1px solid rgba(255, 255, 255, 0.3); /* Brighter border */\n"
"}\n"
"\n"
"/* --- Pressed State --- */\n"
"QPushButton#btnStartDownload:pressed {\n"
"    /* Darker solid color or inverted gradient */\n"
"    background-color: #1e40af; /* Blue-800 */\n"
"    border: 1px solid transparent;\n"
"    \n"
"    /* Slight shift to mimic physical press */\n"
"    padding-top: 22px;\n"
"    padding-bottom: 18px;\n"
"}\n"
"\n"
"/* --- Disabled State (Optional) --- */\n"
"QPushButton#btnStartDownload:disabled {\n"
"    background-color: #1A1A1F;\n"
"    color: #52525b;\n"
"    border: 1px solid #27272a;\n"
"}")
        self.btnStartDownload.setIconSize(QSize(21, 21))
        self.btnStartDownload.setCheckable(True)
        self.label_2 = QLabel(self.download_container)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(220, 340, 51, 51))
        self.label_2.setStyleSheet(u"background-color: rgba(226, 228, 232, 40);\n"
"border-radius: 25px;\n"
"border: 1px solid white;")
        self.download_icon = QLabel(self.download_container)
        self.download_icon.setObjectName(u"download_icon")
        self.download_icon.setGeometry(QRect(235, 356, 21, 21))
        self.download_icon.setFont(font1)
        self.download_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.download_icon.setPixmap(QPixmap(u":/images/download.png"))
        self.download_icon.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.main_container)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.stackedWidget.addWidget(self.download_page)
        self.main_frame.raise_()
        self.metadata_placeholder.raise_()
        self.inputContainer.raise_()
        self.history_page = QWidget()
        self.history_page.setObjectName(u"history_page")
        self.download_history_table = QTableWidget(self.history_page)
        self.download_history_table.setObjectName(u"download_history_table")
        self.download_history_table.setGeometry(QRect(160, 280, 971, 301))
        font11 = QFont()
        font11.setFamilies([u"Inter"])
        font11.setPointSize(11)
        self.download_history_table.setFont(font11)
        self.download_history_table.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.download_history_table.setLayoutDirection(Qt.LeftToRight)
        self.download_history_table.setAutoFillBackground(False)
        self.download_history_table.setStyleSheet(u"")
        self.download_history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.download_history_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.download_history_table.setAutoScroll(False)
        self.download_history_table.setAutoScrollMargin(16)
        self.download_history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.download_history_table.setTabKeyNavigation(True)
        self.download_history_table.setProperty(u"showDropIndicator", False)
        self.download_history_table.setDragDropOverwriteMode(False)
        self.download_history_table.setAlternatingRowColors(False)
        self.download_history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.download_history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.download_history_table.setTextElideMode(Qt.ElideMiddle)
        self.download_history_table.setShowGrid(True)
        self.download_history_table.setGridStyle(Qt.NoPen)
        self.download_history_table.setSortingEnabled(False)
        self.download_history_table.horizontalHeader().setVisible(False)
        self.download_history_table.horizontalHeader().setCascadingSectionResizes(False)
        self.download_history_table.horizontalHeader().setDefaultSectionSize(220)
        self.download_history_table.horizontalHeader().setHighlightSections(False)
        self.download_history_table.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.download_history_table.horizontalHeader().setStretchLastSection(False)
        self.download_history_table.verticalHeader().setVisible(False)
        self.download_history_table.verticalHeader().setCascadingSectionResizes(False)
        self.download_history_table.verticalHeader().setDefaultSectionSize(48)
        self.download_history_table.verticalHeader().setHighlightSections(False)
        self.download_history_table.verticalHeader().setProperty(u"showSortIndicator", False)
        self.download_history_table.verticalHeader().setStretchLastSection(False)
        self.searchHistoryInput = QLineEdit(self.history_page)
        self.searchHistoryInput.setObjectName(u"searchHistoryInput")
        self.searchHistoryInput.setGeometry(QRect(820, 200, 311, 41))
        self.searchHistoryInput.setFont(font8)
        self.searchHistoryInput.setStyleSheet(u"QLineEdit {\n"
"	color: #9ca3af;\n"
"	border-radius: 10px;\n"
"	background-color: #1c1c1e;\n"
"	border: 1px solid #2c2c2e;\n"
"    padding-left: 30px;\n"
"}\n"
"\n"
"QLineEdit::focus {\n"
"	border: 2px solid #2563eb;\n"
"}")
        self.searchHistoryInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.searchHistoryInput.setClearButtonEnabled(True)
        self.label = QLabel(self.history_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(830, 210, 18, 18))
        self.label.setPixmap(QPixmap(u":/images/search.png"))
        self.label.setScaledContents(True)
        self.btnTotalDownloads = QPushButton(self.history_page)
        self.btnTotalDownloads.setObjectName(u"btnTotalDownloads")
        self.btnTotalDownloads.setGeometry(QRect(300, 160, 131, 31))
        font12 = QFont()
        font12.setFamilies([u"JetBrains Mono"])
        font12.setBold(True)
        self.btnTotalDownloads.setFont(font12)
        self.btnTotalDownloads.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.btnTotalDownloads.setStyleSheet(u"background-color: transparent;\n"
"border-radius: 5px;\n"
"color: #8b919d;\n"
"text-align: left;")
        self.btnTotalDownloads.setCheckable(False)
        self.btnHistoryTrash = QPushButton(self.history_page)
        self.btnHistoryTrash.setObjectName(u"btnHistoryTrash")
        self.btnHistoryTrash.setGeometry(QRect(780, 200, 36, 41))
        font13 = QFont()
        font13.setBold(False)
        font13.setItalic(False)
        self.btnHistoryTrash.setFont(font13)
        self.btnHistoryTrash.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnHistoryTrash.setStyleSheet(u"background-color: transparent;\n"
"border: none;")
        self.btnHistoryTrash.setIcon(icon1)
        self.btnHistoryTrash.setIconSize(QSize(20, 20))
        self.btnHistoryTrash.setCheckable(True)
        self.cards = QFrame(self.history_page)
        self.cards.setObjectName(u"cards")
        self.cards.setGeometry(QRect(170, 0, 971, 131))
        self.cards.setStyleSheet(u"background-color: transparent;\n"
"border: none;\n"
"outline: none;")
        self.cards.setFrameShape(QFrame.StyledPanel)
        self.cards.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.cards)
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.storage = QFrame(self.cards)
        self.storage.setObjectName(u"storage")
        self.storage.setStyleSheet(u"QFrame {\n"
"    background-color: rgb(28, 28, 30);\n"
"    border-radius: 12px;\n"
"    border: 1px solid #45475a;\n"
"    padding: 15px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 2px solid rgb(201, 215, 91)\n"
"}")
        self.storage.setFrameShape(QFrame.StyledPanel)
        self.storage.setFrameShadow(QFrame.Raised)
        self.label_3 = QLabel(self.storage)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 10, 161, 31))
        font14 = QFont()
        font14.setFamilies([u"Manrope"])
        font14.setPointSize(11)
        self.label_3.setFont(font14)
        self.label_3.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"padding: 0px;")
        self.label_3.setWordWrap(True)
        self.total_storage_label = QLabel(self.storage)
        self.total_storage_label.setObjectName(u"total_storage_label")
        self.total_storage_label.setGeometry(QRect(20, 40, 111, 21))
        font15 = QFont()
        font15.setFamilies([u"Manrope"])
        font15.setPointSize(18)
        self.total_storage_label.setFont(font15)
        self.total_storage_label.setStyleSheet(u"background-color: transparent;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"padding: 0px;")
        self.total_storage_label.setWordWrap(True)
        self.label_6 = QLabel(self.storage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(230, 20, 61, 61))
        self.label_6.setStyleSheet(u"border: none;\n"
"background-color: transparent;")
        self.label_6.setPixmap(QPixmap(u":/images/hard-drives-fill.png"))

        self.horizontalLayout_5.addWidget(self.storage)

        self.video_files = QFrame(self.cards)
        self.video_files.setObjectName(u"video_files")
        self.video_files.setStyleSheet(u"QFrame {\n"
"    background-color: rgb(28, 28, 30);\n"
"    border-radius: 12px;\n"
"    border: 1px solid #45475a;\n"
"    padding: 15px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 2px solid rgb(59, 130, 246)\n"
"}")
        self.video_files.setFrameShape(QFrame.StyledPanel)
        self.video_files.setFrameShadow(QFrame.Raised)
        self.label_5 = QLabel(self.video_files)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(230, 20, 61, 61))
        self.label_5.setStyleSheet(u"border: none;\n"
"background-color: transparent;")
        self.label_5.setPixmap(QPixmap(u":/images/film-active.png"))
        self.label_9 = QLabel(self.video_files)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 10, 161, 31))
        self.label_9.setFont(font14)
        self.label_9.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"padding: 0px;")
        self.label_9.setWordWrap(True)
        self.total_videos = QLabel(self.video_files)
        self.total_videos.setObjectName(u"total_videos")
        self.total_videos.setGeometry(QRect(20, 40, 111, 21))
        self.total_videos.setFont(font15)
        self.total_videos.setStyleSheet(u"background-color: transparent;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"padding: 0px;")
        self.total_videos.setWordWrap(True)

        self.horizontalLayout_5.addWidget(self.video_files)

        self.audio_files = QFrame(self.cards)
        self.audio_files.setObjectName(u"audio_files")
        self.audio_files.setStyleSheet(u"QFrame {\n"
"    background-color: rgb(28, 28, 30);\n"
"    border-radius: 12px;\n"
"    border: 1px solid #45475a;\n"
"    padding: 15px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 2px solid rgb(129, 140, 248)\n"
"}")
        self.audio_files.setFrameShape(QFrame.StyledPanel)
        self.audio_files.setFrameShadow(QFrame.Raised)
        self.label_7 = QLabel(self.audio_files)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(240, 20, 61, 61))
        self.label_7.setStyleSheet(u"border: none;\n"
"background-color: transparent;")
        self.label_7.setPixmap(QPixmap(u":/images/waveform-active.png"))
        self.label_11 = QLabel(self.audio_files)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 10, 161, 31))
        self.label_11.setFont(font14)
        self.label_11.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"padding: 0px;")
        self.label_11.setWordWrap(True)
        self.total_audios = QLabel(self.audio_files)
        self.total_audios.setObjectName(u"total_audios")
        self.total_audios.setGeometry(QRect(20, 40, 111, 21))
        self.total_audios.setFont(font15)
        self.total_audios.setStyleSheet(u"background-color: transparent;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"padding: 0px;")
        self.total_audios.setWordWrap(True)

        self.horizontalLayout_5.addWidget(self.audio_files)

        self.line = QFrame(self.history_page)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(180, 260, 951, 3))
        self.line.setStyleSheet(u"background-color: rgb(28, 28, 30);")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.logo_text_5 = QLabel(self.history_page)
        self.logo_text_5.setObjectName(u"logo_text_5")
        self.logo_text_5.setGeometry(QRect(180, 148, 121, 41))
        font16 = QFont()
        font16.setFamilies([u"Manrope ExtraBold"])
        font16.setPointSize(24)
        font16.setBold(True)
        self.logo_text_5.setFont(font16)
        self.logo_text_5.setStyleSheet(u"background-color: transparent;\n"
"color: white;")
        self.filter_container = QWidget(self.history_page)
        self.filter_container.setObjectName(u"filter_container")
        self.filter_container.setGeometry(QRect(170, 190, 291, 61))
        self.btnVideo = QPushButton(self.filter_container)
        self.btnVideo.setObjectName(u"btnVideo")
        self.btnVideo.setGeometry(QRect(100, 10, 81, 36))
        font17 = QFont()
        font17.setFamilies([u"Manrope"])
        font17.setBold(True)
        self.btnVideo.setFont(font17)
        self.btnVideo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnVideo.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(28, 28, 30);\n"
"    color: #9ca3af; /* Gray-400 */\n"
"    border: 1px solid rgba(255, 255, 255, 12); /* Subtle Border */\n"
"    border-radius: 15px;\n"
"    padding: 6px 16px;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"    font-family: 'Manrope';\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: white;\n"
"    border: 1px solid rgba(255, 255, 255, 50); /* Brighter border on hover */\n"
"    background-color: #18181b;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #27272a;\n"
"}")
        self.btnVideo.setIconSize(QSize(14, 14))
        self.btnVideo.setCheckable(True)
        self.btnAllMedia = QPushButton(self.filter_container)
        self.btnAllMedia.setObjectName(u"btnAllMedia")
        self.btnAllMedia.setGeometry(QRect(10, 10, 81, 36))
        self.btnAllMedia.setFont(font17)
        self.btnAllMedia.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnAllMedia.setStyleSheet(u"QPushButton {\n"
"    background-color: #3B82F6; /* Primary Blue */\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 15px; /* Fully rounded (Half of height approx) */\n"
"    padding: 6px 16px;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"    font-family: 'Manrope';\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2563EB; /* Slightly darker blue */\n"
"}")
        self.btnAllMedia.setIconSize(QSize(14, 14))
        self.btnAllMedia.setCheckable(True)
        self.btnAudio = QPushButton(self.filter_container)
        self.btnAudio.setObjectName(u"btnAudio")
        self.btnAudio.setGeometry(QRect(190, 10, 81, 36))
        self.btnAudio.setFont(font17)
        self.btnAudio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnAudio.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(28, 28, 30);\n"
"    color: #9ca3af; /* Gray-400 */\n"
"    border: 1px solid rgba(255, 255, 255, 12); /* Subtle Border */\n"
"    border-radius: 15px;\n"
"    padding: 6px 16px;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"    font-family: 'Manrope';\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: white;\n"
"    border: 1px solid rgba(255, 255, 255, 50); /* Brighter border on hover */\n"
"    background-color: #18181b;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #27272a;\n"
"}")
        self.btnAudio.setIconSize(QSize(14, 14))
        self.btnAudio.setCheckable(True)
        self.stackedWidget.addWidget(self.history_page)
        self.files_page = QWidget()
        self.files_page.setObjectName(u"files_page")
        self.stackedWidget.addWidget(self.files_page)
        self.version_ffmpeg_det = QLabel(self.sidebar_2)
        self.version_ffmpeg_det.setObjectName(u"version_ffmpeg_det")
        self.version_ffmpeg_det.setGeometry(QRect(240, 50, 41, 21))
        self.version_ffmpeg_det.setFont(font)
        self.version_ffmpeg_det.setStyleSheet(u"color: #4B5563;\n"
"background-color: transparent;")
        self.highlight_bar = QWidget(self.sidebar_2)
        self.highlight_bar.setObjectName(u"highlight_bar")
        self.highlight_bar.setGeometry(QRect(870, 20, 261, 51))
        self.highlight_bar.setStyleSheet(u"/* 1. The Container (Outer Shell) */\n"
"#highlight_bar {\n"
"    background-color: #1a1a1f;   /* Your requested container color */\n"
"    border-radius: 25px;         /* Fully rounded outer edges */\n"
"    border: 1px solid #2b2b2b;   /* Subtle border for the container */\n"
"}\n"
"\n"
"/* 2. The Sliding Pill (Active Highlight) */\n"
"/* Using QFrame selector ensures the radius is applied */\n"
"QFrame#anim_pill {\n"
"    background-color: #0f0f12;   /* Your requested active color */\n"
"    border-radius: 18px;         /* radius must be < container radius to fit */\n"
"    border: 1px solid #333333;   /* Border around the pill */\n"
"}\n"
"\n"
"/* 3. The Buttons */\n"
"#btnNavDashboard, #btnNavHistory {\n"
"    background: transparent;     \n"
"    border: none;\n"
"    color: #888888;              \n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    border-radius: 18px;         /* Match the pill radius */\n"
"}\n"
"\n"
"/* 4. Text Colors */\n"
"#btnNavDashboard:hover, #btnNavHistory:hover {\n"
"  "
                        "  color: #bbbbbb;\n"
"}\n"
"\n"
"#btnNavDashboard:checked, #btnNavHistory:checked {\n"
"    color: #ffffff;              \n"
"}")
        self.horizontalLayout = QHBoxLayout(self.highlight_bar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnNavDashboard = QPushButton(self.highlight_bar)
        self.btnNavDashboard.setObjectName(u"btnNavDashboard")
        self.btnNavDashboard.setFont(font3)
        self.btnNavDashboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnNavDashboard.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/images/magic-wand.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnNavDashboard.setIcon(icon2)
        self.btnNavDashboard.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnNavDashboard)

        self.btnNavHistory = QPushButton(self.highlight_bar)
        self.btnNavHistory.setObjectName(u"btnNavHistory")
        self.btnNavHistory.setFont(font3)
        self.btnNavHistory.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnNavHistory.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/images/clock-gray.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnNavHistory.setIcon(icon3)
        self.btnNavHistory.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnNavHistory)

        self.mp4_icon_2 = QLabel(self.sidebar_2)
        self.mp4_icon_2.setObjectName(u"mp4_icon_2")
        self.mp4_icon_2.setGeometry(QRect(190, 30, 41, 41))
        self.mp4_icon_2.setFont(font1)
        self.mp4_icon_2.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_2.setPixmap(QPixmap(u":/images/vac-logo.png"))
        self.mp4_icon_2.setScaledContents(True)
        self.logo_text_4 = QLabel(self.sidebar_2)
        self.logo_text_4.setObjectName(u"logo_text_4")
        self.logo_text_4.setGeometry(QRect(240, 30, 41, 21))
        self.logo_text_4.setFont(font8)
        self.logo_text_4.setStyleSheet(u"background-color: transparent;\n"
"color: white;")
        self.progressBar = QProgressBar(self.sidebar_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(870, 80, 260, 10))
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setMinimumSize(QSize(200, 10))
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"	background-color: rgb(28, 28, 30);\n"
"    border: none;\n"
"    border-radius: 4px; /* Rounded ends */\n"
"    height: 6px; /* Force it to be thin */\n"
"    text-align: center; /* Required property */\n"
"    color: transparent; /* Hides the text inside the bar */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #0A84FF; /* The active blue bar */\n"
"    border-radius: 3px;\n"
"}")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.sidebar_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.iconLabel.setText("")
        self.urlInput.setText("")
        self.urlInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Paste or Enter Link", None))
        self.pasteBtn.setText(QCoreApplication.translate("MainWindow", u"PASTE", None))
        self.btnAddQueue.setText("")
        self.btnFormatVideo.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.btnFormatAudio.setText(QCoreApplication.translate("MainWindow", u"Audio", None))
        self.logo_text_3.setText(QCoreApplication.translate("MainWindow", u"FORMAT", None))
        self.mp3_icon.setText("")
        self.mp4_icon.setText("")
        self.logo_text_7.setText(QCoreApplication.translate("MainWindow", u"MP4", None))
        self.logo_text_8.setText(QCoreApplication.translate("MainWindow", u"MP3", None))
        self.logo_text_6.setText(QCoreApplication.translate("MainWindow", u"QUALITY", None))
        self.comboQuality.setItemText(0, QCoreApplication.translate("MainWindow", u"4k", None))

        self.logo_text_10.setText(QCoreApplication.translate("MainWindow", u"OUTPUT CONFIGURATION", None))
        self.mp4_icon_3.setText("")
        self.logo_text_9.setText(QCoreApplication.translate("MainWindow", u"System Log", None))
        self.mp3_icon_2.setText("")
        self.download_queue.setText(QCoreApplication.translate("MainWindow", u"Conversion Queue", None))
        self.btnClearQueue.setText("")
        self.btnStartDownload.setText(QCoreApplication.translate("MainWindow", u"Start\n"
"Conversion", None))
#if QT_CONFIG(shortcut)
        self.btnStartDownload.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText("")
        self.download_icon.setText("")
        self.searchHistoryInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search archives...", None))
        self.label.setText("")
        self.btnTotalDownloads.setText(QCoreApplication.translate("MainWindow", u"3 Items", None))
        self.btnHistoryTrash.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TOTAL STORAGE", None))
        self.total_storage_label.setText(QCoreApplication.translate("MainWindow", u"48.5 GB", None))
        self.label_6.setText("")
        self.label_5.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"VIDEO FILES", None))
        self.total_videos.setText(QCoreApplication.translate("MainWindow", u"125", None))
        self.label_7.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"AUDIO FILES", None))
        self.total_audios.setText(QCoreApplication.translate("MainWindow", u"512", None))
        self.logo_text_5.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.btnVideo.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.btnAllMedia.setText(QCoreApplication.translate("MainWindow", u"All Media", None))
        self.btnAudio.setText(QCoreApplication.translate("MainWindow", u"Audio", None))
        self.version_ffmpeg_det.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
        self.btnNavDashboard.setText(QCoreApplication.translate("MainWindow", u" Studio", None))
        self.btnNavHistory.setText(QCoreApplication.translate("MainWindow", u" History", None))
        self.mp4_icon_2.setText("")
        self.logo_text_4.setText(QCoreApplication.translate("MainWindow", u"VAC", None))
    # retranslateUi

