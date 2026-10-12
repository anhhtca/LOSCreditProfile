# -*- coding: utf-8 -*-
"""
stamp_utils.py
Tạo con dấu đỏ (rubber stamp) và chữ ký mực xanh (signature) thực tế
cho hồ sơ tín dụng Vinamilk & Agribank phục vụ kiểm thử OCR.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_TIMES = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
FONT_PATH_ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def create_circular_stamp(outer_text, center_text, sub_center_text="", size=360, stamp_type="company"):
    """
    Tạo con dấu tròn màu đỏ mô phỏng con dấu doanh nghiệp / ngân hàng
    """
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Màu mực đỏ con dấu thực tế (hơi lem nhẹ đặc trưng mực cao su)
    red_color = (205, 28, 38, 235)
    center = size / 2.0
    radius = size / 2.0 - 15

    # Vòng tròn ngoài (đậm) và vòng tròn trong (mảnh)
    draw.ellipse([15, 15, size - 15, size - 15], outline=red_color, width=5)
    draw.ellipse([25, 25, size - 25, size - 25], outline=red_color, width=2)

    # Font chữ
    try:
        font_curve = ImageFont.truetype(FONT_PATH_ARIAL, 20)
        font_center = ImageFont.truetype(FONT_PATH_TIMES, 22)
        font_sub = ImageFont.truetype(FONT_PATH_ARIAL, 16)
        font_star = ImageFont.truetype(FONT_PATH_TIMES, 28)
    except Exception:
        font_curve = ImageFont.load_default()
        font_center = font_curve
        font_sub = font_curve
        font_star = font_curve

    # Vẽ chữ uốn lượn theo cung tròn trên
    chars = list(outer_text)
    n_chars = len(chars)
    if n_chars > 0:
        # Cung độ uốn cong
        total_angle = min(220, n_chars * 11)
        start_angle = -90 - total_angle / 2.0
        step_angle = total_angle / max(1, n_chars - 1)
        r_text = radius - 24

        for i, char in enumerate(chars):
            ang_deg = start_angle + i * step_angle
            ang_rad = math.radians(ang_deg)
            cx = center + r_text * math.cos(ang_rad)
            cy = center + r_text * math.sin(ang_rad)

            # Tạo ảnh nhỏ cho từng ký tự để xoay
            char_img = Image.new("RGBA", (40, 40), (255, 255, 255, 0))
            cdraw = ImageDraw.Draw(char_img)
            bbox = cdraw.textbbox((0, 0), char, font=font_curve)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            cdraw.text(((40 - w) / 2.0, (40 - h) / 2.0), char, font=font_curve, fill=red_color)

            # Xoay ký tự vuông góc với tiếp tuyến bán kính
            rot_deg = - (ang_deg + 90)
            rotated_char = char_img.rotate(rot_deg, resample=Image.BICUBIC, expand=True)
            rw, rh = rotated_char.size
            img.paste(rotated_char, (int(cx - rw / 2.0), int(cy - rh / 2.0)), rotated_char)

    # Vẽ ngôi sao ở giữa
    star = "★"
    s_box = draw.textbbox((0, 0), star, font=font_star)
    sw = s_box[2] - s_box[0]
    draw.text((center - sw / 2.0, center - 60), star, font=font_star, fill=red_color)

    # Chữ ở tâm con dấu (Tên công ty / Chi nhánh)
    c_box = draw.textbbox((0, 0), center_text, font=font_center)
    cw = c_box[2] - c_box[0]
    draw.text((center - cw / 2.0, center - 16), center_text, font=font_center, fill=red_color)

    # Chữ phụ ở tâm (Mã số thuế / Địa phương)
    if sub_center_text:
        sub_box = draw.textbbox((0, 0), sub_center_text, font=font_sub)
        subw = sub_box[2] - sub_box[0]
        draw.text((center - subw / 2.0, center + 20), sub_center_text, font=font_sub, fill=red_color)

    # Vòng tròn trong bảo vệ tâm
    draw.ellipse([center - 90, center - 90, center + 90, center + 90], outline=red_color, width=1)

    return img


def create_signature_image(name="Mai Kiều Liên", width=220, height=80):
    """
    Tạo chữ ký tay màu xanh mực bút bi thực tế
    """
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Màu mực xanh bút bi Parker / Thiên Long
    blue_color = (0, 48, 145, 240)

    # Vẽ các đường lượn chữ ký mô phỏng
    points = [
        (25, 55), (45, 25), (60, 45), (80, 20), (100, 50),
        (130, 25), (150, 40), (180, 15), (200, 60), (140, 68), (70, 70), (190, 65)
    ]
    # Nối các điểm bằng đường cong bezier hoặc line mảnh
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=blue_color, width=3)

    # Thêm gạch dưới cách điệu
    draw.line([(30, 72), (205, 68)], fill=blue_color, width=2)

    return img
