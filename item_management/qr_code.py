import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import numpy as np  # pip install numpy
import cv2  # pip install opencv-python
from imutils.video import VideoStream
import imutils
from .models import QRCODE


class Stream:
    def __init__(self):
        self.cap = VideoStream().start()
        self.barcode_type = None
        self.barcode_data = None

    def stream(self, request):

        img = self.cap.read()
        # img = imutils.resize(img, width=500)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        decoded = pyzbar.decode(gray)

        for d in decoded:
            x, y, w, h = d.rect
            self.barcode_data = d.data.decode("UTF-8")
            self.barcode_type = d.type

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            text = '%s (%s)' % (self.barcode_data, self.barcode_type)
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

            if self.barcode_data != '' and self.barcode_type == 'QRCODE':
                qr_db = QRCODE.objects

                # token = request.GET.get('csrfmiddlewaretoken')[:224]
                # qr_db.create(qr_id=token, qr_decode=self.barcode_data)
                return False
        # cv2.imshow('img', img)
        _, jpeg = cv2.imencode('.jpg', img)

        return jpeg.tobytes()

    def read_code(self):
        pass
