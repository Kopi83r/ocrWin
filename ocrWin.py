import io
import os
import sys 
import mss
import pyperclip
import pytesseract
import numpy as np
import cv2

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

# 👉 SET THIS TO YOUR TESSERACT PATH
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

pytesseract.pytesseract.tesseract_cmd = os.path.join(
    BASE_DIR, "tesseract", "tesseract.exe"
)
os.environ["TESSDATA_PREFIX"] = os.path.join(BASE_DIR, "tesseract", "tessdata")


class SnippingTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        # --- SCREENSHOT ---
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)

            self.pil_img = Image.frombytes(
                "RGB", sct_img.size, sct_img.bgra, "raw", "BGRX"
            )

            buffer = io.BytesIO()
            self.pil_img.save(buffer, format="PNG")
            self.screen_pixmap = QtGui.QPixmap()
            self.screen_pixmap.loadFromData(buffer.getvalue(), "PNG")

            self.offset_x = monitor["left"]
            self.offset_y = monitor["top"]

        # --- WINDOW ---
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )

        self.setGeometry(
            self.offset_x,
            self.offset_y,
            self.screen_pixmap.width(),
            self.screen_pixmap.height(),
        )

        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawPixmap(0, 0, self.screen_pixmap)

        path = QtGui.QPainterPath()
        path.addRect(QtCore.QRectF(self.rect()))

        if not self.begin.isNull() and not self.end.isNull():
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            w = abs(self.begin.x() - self.end.x())
            h = abs(self.begin.y() - self.end.y())

            selection_path = QtGui.QPainterPath()
            selection_path.addRect(x1, y1, w, h)
            path = path.subtracted(selection_path)

            qp.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
            qp.setBrush(QtCore.Qt.NoBrush)
            qp.drawRect(x1, y1, w, h)

        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0, 100))
        qp.drawPath(path)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()
        self.process_ocr()

    def process_ocr(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        if (x2 - x1) < 10 or (y2 - y1) < 10:
            QtWidgets.QApplication.quit()
            return

        try:
            cropped = self.pil_img.crop((x1, y1, x2, y2))

            # --- 🔥 OCR PREPROCESSING (BIG IMPROVEMENT) ---
            img = np.array(cropped)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # upscale for small text
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # denoise
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            # adaptive threshold (better than fixed)
            thresh = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31, 2
            )

            # --- OCR CONFIG ---
            config = "--oem 3 --psm 6"

            text = pytesseract.image_to_string(
                thresh,
                config=config,
                lang="eng+pol"
            )
            clean_text = text.strip()

            if clean_text:
                pyperclip.copy(clean_text)
            else:
                pyperclip.copy("")

        except Exception as e:
            print("Error:", e)

        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    window = SnippingTool()
    sys.exit(app.exec_())