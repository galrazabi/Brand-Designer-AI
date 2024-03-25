from io import BytesIO
import cv2, os
import numpy as np
from db import *

def make_logo_shirt(name):
    response = None

    logo = get_company_logo(name)
    binary_data = base64.b64decode(logo)
    nparr = np.frombuffer(binary_data, np.uint8)
    logo = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    tshirt = cv2.imread('./data/shirt.png')

    if logo is not None and logo.shape[0] > 0 and logo.shape[1] > 0:
        logo = cv2.resize(logo, (260, 260))  

        x_offset = 380  
        y_offset = 290  
        rows, cols, _ = logo.shape
        roi = tshirt[y_offset:y_offset + rows, x_offset:x_offset + cols]

        logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        _, logo_mask = cv2.threshold(logo_gray, 200, 255, cv2.THRESH_BINARY_INV)
        logo_mask_inv = cv2.bitwise_not(logo_mask)

        tshirt_bg = cv2.bitwise_and(roi, roi, mask=logo_mask_inv)
        logo_fg = cv2.bitwise_and(logo, logo, mask=logo_mask)
        dst = cv2.add(tshirt_bg, logo_fg)
        tshirt[y_offset:y_offset + rows, x_offset:x_offset + cols] = dst

    cv2.imwrite("temp_image.png", tshirt)
    with open("temp_image.png", "rb") as f:
        image_blob = f.read()
    
    return image_blob



