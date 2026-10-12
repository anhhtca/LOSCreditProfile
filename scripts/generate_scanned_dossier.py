# -*- coding: utf-8 -*-
"""
generate_scanned_dossier.py
Sinh trọn bộ tài liệu hồ sơ tín dụng Vinamilk (VNM) dạng PDF Scanned
đáp ứng chuẩn nghiệp vụ của Agribank SDTN phục vụ kiểm thử OCR và AI Analysis.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from stamp_utils import create_circular_stamp, create_signature_image

# 1. Đăng ký Font chữ tiếng Việt hệ thống macOS
BASE_FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Times", f"{BASE_FONT_DIR}/Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("Times-Bold", f"{BASE_FONT_DIR}/Times New Roman Bold.ttf"))
pdfmetrics.registerFont(TTFont("Times-Italic", f"{BASE_FONT_DIR}/Times New Roman Italic.ttf"))
pdfmetrics.registerFont(TTFont("Times-BoldItalic", f"{BASE_FONT_DIR}/Times New Roman Bold Italic.ttf"))

pdfmetrics.registerFont(TTFont("Arial", f"{BASE_FONT_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{BASE_FONT_DIR}/Arial Bold.ttf"))

# 2. Thư mục đầu ra
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_BASE = os.path.join(PROJECT_ROOT, "documents", "7900.001.23.DN.0300588569")
TEMP_DIR = os.path.join(PROJECT_ROOT, "temp_stamps")
os.makedirs(TEMP_DIR, exist_ok=True)

# 3. Tạo sẵn con dấu và chữ ký mẫu
STAMP_VNM = os.path.join(TEMP_DIR, "stamp_vnm.png")
STAMP_KPMG = os.path.join(TEMP_DIR, "stamp_kpmg.png")
STAMP_AGRI = os.path.join(TEMP_DIR, "stamp_agri.png")
STAMP_GOV = os.path.join(TEMP_DIR, "stamp_gov.png")

SIG_MKL = os.path.join(TEMP_DIR, "sig_mkl.png")
SIG_LTL = os.path.join(TEMP_DIR, "sig_ltl.png")
SIG_NHP = os.path.join(TEMP_DIR, "sig_nhp.png")
SIG_AUDITOR = os.path.join(TEMP_DIR, "sig_auditor.png")

create_circular_stamp("CÔNG TY CỔ PHẦN SỮA VIỆT NAM", "VINAMILK", "MST: 0300588569").save(STAMP_VNM)
create_circular_stamp("CÔNG TY TNHH KPMG VIỆT NAM", "KPMG", "KIỂM TOÁN VIÊN").save(STAMP_KPMG)
create_circular_stamp("NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VIỆT NAM", "AGRIBANK", "CN TP. HỒ CHÍ MINH").save(STAMP_AGRI)
create_circular_stamp("SỞ KẾ HOẠCH VÀ ĐẦU TƯ", "TP. HỒ CHÍ MINH", "PHÒNG ĐKKD").save(STAMP_GOV)

create_signature_image("Mai Kiều Liên").save(SIG_MKL)
create_signature_image("Lê Thành Liêm").save(SIG_LTL)
create_signature_image("Nguyễn Hạnh Phúc").save(SIG_NHP)
create_signature_image("KPMG Auditor").save(SIG_AUDITOR)


def get_styles():
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.fontName = "Times"
    normal.fontSize = 10
    normal.leading = 14

    title_style = ParagraphStyle(
        "DocTitle",
        parent=normal,
        fontName="Times-Bold",
        fontSize=13,
        leading=17,
        alignment=1, # Center
        spaceAfter=10
    )

    header_left = ParagraphStyle(
        "HeaderLeft",
        parent=normal,
        fontName="Times-Bold",
        fontSize=9.5,
        leading=13,
        alignment=0
    )

    header_right = ParagraphStyle(
        "HeaderRight",
        parent=normal,
        fontName="Times-Bold",
        fontSize=9.5,
        leading=13,
        alignment=1
    )

    body_text = ParagraphStyle(
        "BodyTextVN",
        parent=normal,
        fontSize=10,
        leading=15,
        alignment=4 # Justify
    )

    table_text = ParagraphStyle(
        "TableText",
        parent=normal,
        fontSize=9,
        leading=12
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=normal,
        fontName="Times-Bold",
        fontSize=9,
        leading=12,
        alignment=1
    )

    return {
        "title": title_style,
        "h_left": header_left,
        "h_right": header_right,
        "body": body_text,
        "table": table_text,
        "table_h": table_header,
        "normal": normal
    }


def add_official_header(elements, styles, org_name, doc_code, location_date):
    """Tạo Header Quốc hiệu & Tiêu ngữ chuẩn công văn Việt Nam"""
    data = [
        [
            Paragraph(f"<b>{org_name}</b><br/>Số: {doc_code}", styles["h_left"]),
            Paragraph("<b>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</b><br/><b><u>Độc lập - Tự do - Hạnh phúc</u></b><br/><i>" + location_date + "</i>", styles["h_right"])
        ]
    ]
    t = Table(data, colWidths=[240, 280])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))


def add_signature_block(elements, styles, left_title, left_name, right_title, right_name, stamp_path=None, sig_path=None):
    """Tạo khối chữ ký người có thẩm quyền kèm con dấu tròn đỏ và chữ ký tay mực xanh"""
    data = [
        [
            Paragraph(f"<b>{left_title}</b>", styles["h_right"]),
            Paragraph(f"<b>{right_title}</b>", styles["h_right"])
        ],
        [
            RLImage(SIG_LTL, width=120, height=45) if left_name else Paragraph("", styles["normal"]),
            RLImage(sig_path if sig_path else SIG_MKL, width=120, height=45)
        ],
        [
            Paragraph(f"<b>{left_name}</b>", styles["h_right"]) if left_name else Paragraph("", styles["normal"]),
            Paragraph(f"<b>{right_name}</b>", styles["h_right"])
        ]
    ]
    t = Table(data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(Spacer(1, 15))
    elements.append(t)


# ==============================================================================
# 4. CÁC HÀM TẠO TỪNG VĂN BẢN CỤ THỂ
# ==============================================================================

def create_doc_A11(output_path, styles):
    """A.1.1: Giấy chứng nhận ĐKDN lần 33"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []

    add_official_header(elements, styles, "SỞ KẾ HOẠCH VÀ ĐẦU TƯ<br/>TP. HỒ CHÍ MINH", "0300588569/ĐKKD", "TP. Hồ Chí Minh, ngày 27 tháng 12 năm 2022")

    elements.append(Paragraph("GIẤY CHỨNG NHẬN ĐĂNG KÝ DOANH NGHIỆP<br/>CÔNG TY CỔ PHẦN", styles["title"]))
    elements.append(Paragraph("<b>Mã số doanh nghiệp: 0300588569</b><br/><i>Đăng ký lần đầu: ngày 20 tháng 11 năm 2003<br/>Đăng ký thay đổi lần thứ 33: ngày 27 tháng 12 năm 2022</i>", ParagraphStyle('C', parent=styles['title'], fontSize=11, leading=15)))
    elements.append(Spacer(1, 10))

    content = """
    <b>1. Tên công ty:</b><br/>
    - Tên công ty viết bằng tiếng Việt: <b>CÔNG TY CỔ PHẦN SỮA VIỆT NAM</b><br/>
    - Tên công ty viết bằng tiếng nước ngoài: VIETNAM DAIRY PRODUCTS JOINT STOCK COMPANY<br/>
    - Tên công ty viết tắt: <b>VINAMILK (Mã CK: VNM)</b><br/><br/>
    <b>2. Địa chỉ trụ sở chính:</b> Số 10 Tân Trào, Phường Tân Phú, Quận 7, Thành phố Hồ Chí Minh, Việt Nam.<br/>
    - Điện thoại: (84-28) 54 155 555 | Email: vinamilk@vinamilk.com.vn | Website: www.vinamilk.com.vn<br/><br/>
    <b>3. Vốn điều lệ:</b> <b>20.899.554.450.000 VNĐ</b><br/>
    - Bằng chữ: <i>Hai mươi nghìn tám trăm chín mươi chín tỷ năm trăm năm mươi tư triệu bốn trăm năm mươi nghìn đồng</i>.<br/>
    - Mệnh giá cổ phần: 10.000 đồng/cổ phần. Tổng số cổ phần: 2.089.955.445 cổ phần.<br/><br/>
    <b>4. Người đại diện theo pháp luật:</b><br/>
    - Họ và tên: <b>MAI KIỀU LIÊN</b> - Giới tính: Nữ<br/>
    - Chức danh: <b>Tổng Giám đốc</b><br/>
    - Sinh ngày: 01/09/1953 - Dân tộc: Kinh - Quốc tịch: Việt Nam<br/>
    - Số định danh cá nhân / CCCD: <b>079153001289</b> cấp ngày 10/05/2021 tại Cục Cảnh sát QLHC về TTXH.<br/>
    - Nơi thường trú: Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh.<br/><br/>
    <b>5. Ngành nghề kinh doanh chính:</b> Chế biến sữa và các sản phẩm từ sữa (Mã ngành: 1050 - Chính); Chăn nuôi bò sữa; Bán buôn sữa và các sản phẩm từ sữa.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TRƯỞNG PHÒNG ĐĂNG KÝ KINH DOANH", "Nguyễn Thị Phương Thảo", STAMP_GOV, SIG_NHP)
    doc.build(elements)


def create_doc_A14(output_path, styles):
    """A.1.4: Điều lệ tổ chức và hoạt động (Trích lục)"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "01/2022/ĐL-VNM", "TP. Hồ Chí Minh, ngày 26 tháng 04 năm 2022")
    elements.append(Paragraph("TRÍCH LỤC ĐIỀU LỆ TỔ CHỨC VÀ HOẠT ĐỘNG<br/>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (SỬA ĐỔI LẦN THỨ 14)", styles["title"]))
    content = """
    <b>Căn cứ Luật Doanh nghiệp số 59/2020/QH14 và Nghị quyết ĐHĐCĐ thường niên năm 2022;</b><br/><br/>
    <b>Điều 13. Quyền hạn của Hội đồng Quản trị về Vay vốn và Cấp tín dụng:</b><br/>
    1. Hội đồng quản trị có quyền quyết định các khoản vay, phát hành trái phiếu, mở hạn mức tín dụng và các biện pháp bảo đảm tiền vay tại các Ngân hàng thương mại phục vụ hoạt động sản xuất kinh doanh có giá trị từ 10% đến 50% tổng giá trị tài sản của Công ty ghi trong Báo cáo tài chính gần nhất.<br/>
    2. Tổng Giám đốc là người đại diện theo pháp luật được ủy quyền tổ chức thực hiện, đàm phán và ký kết các Hợp đồng tín dụng, Hợp đồng thế chấp tài sản, Khế ước nhận nợ với các Tổ chức tín dụng theo Nghị quyết của Hội đồng Quản trị.<br/><br/>
    <b>Điều 24. Người đại diện theo pháp luật:</b><br/>
    Công ty có 02 người đại diện theo pháp luật bao gồm: Chủ tịch Hội đồng Quản trị và Tổng Giám đốc. Tổng Giám đốc đại diện cho Công ty trong các quan hệ tố tụng, giao dịch kinh tế, hợp đồng tín dụng và quản lý điều hành hoạt động thường nhật.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "CHỦ TỊCH HỘI ĐỒNG QUẢN TRỊ", "Nguyễn Hạnh Phúc", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_A15(output_path, styles):
    """A.1.5: Nghị quyết HĐQT bổ nhiệm Tổng Giám đốc"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "HỘI ĐỒNG QUẢN TRỊ<br/>CTCP SỮA VIỆT NAM", "08/NQ-CTS.HĐQT/2022", "TP. Hồ Chí Minh, ngày 26 tháng 04 năm 2022")
    elements.append(Paragraph("NGHỊ QUYẾT HỘI ĐỒNG QUẢN TRỊ<br/>V/v: Bổ nhiệm Tổng Giám đốc nhiệm kỳ 2022 - 2026", styles["title"]))
    content = """
    <b>HỘI ĐỒNG QUẢN TRỊ CÔNG TY CỔ PHẦN SỮA VIỆT NAM</b><br/>
    - Căn cứ Điều lệ Công ty Cổ phần Sữa Việt Nam;<br/>
    - Căn cứ Biên bản họp Hội đồng Quản trị số 07/BB-CTS.HĐQT/2022 ngày 26/04/2022.<br/><br/>
    <b>QUYẾT NGHỊ:</b><br/>
    <b>Điều 1:</b> Tái bổ nhiệm Bà <b>MAI KIỀU LIÊN</b> giữ chức danh <b>Tổng Giám đốc</b> Công ty Cổ phần Sữa Việt Nam nhiệm kỳ 2022 - 2026.<br/>
    <b>Điều 2:</b> Bà Mai Kiều Liên thực hiện các quyền và nghĩa vụ của Tổng Giám đốc theo quy định của pháp luật và Điều lệ Công ty; là người đại diện theo pháp luật đại diện ký kết các Hợp đồng tín dụng, Hợp đồng thế chấp với các Ngân hàng.<br/>
    <b>Điều 3:</b> Quyết định có hiệu lực thi hành kể từ ngày ký.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TM. HỘI ĐỒNG QUẢN TRỊ<br/>CHỦ TỊCH", "Nguyễn Hạnh Phúc", STAMP_VNM, SIG_NHP)
    doc.build(elements)


def create_doc_A16(output_path, styles):
    """A.1.6: Quyết định bổ nhiệm Kế toán trưởng"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "TỔNG GIÁM ĐỐC<br/>CTCP SỮA VIỆT NAM", "15/QĐ-CTS/2021", "TP. Hồ Chí Minh, ngày 10 tháng 01 năm 2021")
    elements.append(Paragraph("QUYẾT ĐỊNH BỔ NHIỆM<br/>KẾ TOÁN TRƯỞNG CÔNG TY CỔ PHẦN SỮA VIỆT NAM", styles["title"]))
    content = """
    <b>TỔNG GIÁM ĐỐC CÔNG TY CỔ PHẦN SỮA VIỆT NAM</b><br/>
    - Căn cứ Luật Kế toán số 88/2015/QH13 và Điều lệ Công ty;<br/>
    - Căn cứ Nghị quyết Hội đồng Quản trị phê duyệt cơ cấu nhân sự quản lý.<br/><br/>
    <b>QUYẾT ĐỊNH:</b><br/>
    <b>Điều 1:</b> Bổ nhiệm Ông <b>LÊ THÀNH LIÊM</b> giữ chức vụ <b>Giám đốc Điều hành Tài chính kiêm Kế toán trưởng</b> Công ty Cổ phần Sữa Việt Nam.<br/>
    <b>Điều 2:</b> Ông Lê Thành Liêm có trách nhiệm phụ trách công tác kế toán, quản lý tài chính, kiểm soát dòng tiền và ký duyệt các báo cáo tài chính, chứng từ giải ngân vay vốn tại các Ngân hàng.<br/>
    <b>Điều 3:</b> Quyết định có hiệu lực kể từ ngày ký.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_A18(output_path, styles):
    """A.1.8: Danh sách cổ đông lớn & HĐQT"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "03/2023/VNM-CĐ", "TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023")
    elements.append(Paragraph("DANH SÁCH CỔ ĐÔNG LỚN VÀ THÀNH VIÊN HĐQT<br/><i>(Trích từ Báo cáo tình hình quản trị công ty kiểm toán năm 2023)</i>", styles["title"]))

    table_data = [
        [Paragraph("<b>STT</b>", styles["table_h"]), Paragraph("<b>Tên Cổ đông / Thành viên</b>", styles["table_h"]), Paragraph("<b>Chức vụ / Tư cách</b>", styles["table_h"]), Paragraph("<b>Số lượng cổ phần</b>", styles["table_h"]), Paragraph("<b>Tỷ lệ (%)</b>", styles["table_h"])],
        [Paragraph("1", styles["table"]), Paragraph("Tổng công ty Đầu tư & Kinh doanh Vốn Nhà nước (SCIC)", styles["table"]), Paragraph("Cổ đông Nhà nước lớn nhất", styles["table"]), Paragraph("752.476.602", styles["table"]), Paragraph("36.00%", styles["table"])],
        [Paragraph("2", styles["table"]), Paragraph("F&N Dairy Investments Pte. Ltd (Singapore)", styles["table"]), Paragraph("Cổ đông chiến lược ngoại", styles["table"]), Paragraph("369.753.803", styles["table"]), Paragraph("17.69%", styles["table"])],
        [Paragraph("3", styles["table"]), Paragraph("Platinum Victory Pte. Ltd (Singapore)", styles["table"]), Paragraph("Cổ đông lớn ngoại", styles["table"]), Paragraph("221.856.553", styles["table"]), Paragraph("10.62%", styles["table"])],
        [Paragraph("4", styles["table"]), Paragraph("F&Nbev Manufacturing Pte. Ltd", styles["table"]), Paragraph("Cổ đông ngoại", styles["table"]), Paragraph("56.428.797", styles["table"]), Paragraph("2.70%", styles["table"])],
        [Paragraph("5", styles["table"]), Paragraph("Bà Mai Kiều Liên", styles["table"]), Paragraph("Thành viên HĐQT, Tổng Giám đốc", styles["table"]), Paragraph("6.421.412", styles["table"]), Paragraph("0.31%", styles["table"])],
        [Paragraph("6", styles["table"]), Paragraph("Các cổ đông đại chúng khác", styles["table"]), Paragraph("Tổ chức & cá nhân", styles["table"]), Paragraph("683.018.278", styles["table"]), Paragraph("32.68%", styles["table"])],
        [Paragraph("<b>TỔNG</b>", styles["table_h"]), Paragraph("<b>Toàn bộ cổ phần lưu hành</b>", styles["table_h"]), Paragraph("-", styles["table_h"]), Paragraph("<b>2.089.955.445</b>", styles["table_h"]), Paragraph("<b>100.00%</b>", styles["table_h"])],
    ]
    t = Table(table_data, colWidths=[30, 210, 120, 100, 60])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (3,1), (4,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    add_signature_block(elements, styles, "KẾ TOÁN TRƯỞNG", "Lê Thành Liêm", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_A19(output_path, styles):
    """A.1.9: Bảng kê khai thông tin người có liên quan"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "04/2023/VNM-LQ", "TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023")
    elements.append(Paragraph("BẢNG KÊ KHAI DANH SÁCH NGƯỜI CÓ LIÊN QUAN<br/><i>(Theo quy định của Luật các TCTD phục vụ cấp tín dụng tại Agribank)</i>", styles["title"]))

    table_data = [
        [Paragraph("<b>STT</b>", styles["table_h"]), Paragraph("<b>Tên tổ chức / Cá nhân liên quan</b>", styles["table_h"]), Paragraph("<b>Mối quan hệ với Vinamilk</b>", styles["table_h"]), Paragraph("<b>Mã số thuế / Số CCCD</b>", styles["table_h"]), Paragraph("<b>Tỷ lệ vốn (%)</b>", styles["table_h"])],
        [Paragraph("1", styles["table"]), Paragraph("CTCP Giống bò sữa Mộc Châu (MCM)", styles["table"]), Paragraph("Công ty con (sở hữu gián tiếp)", styles["table"]), Paragraph("0100104191", styles["table"]), Paragraph("59.3%", styles["table"])],
        [Paragraph("2", styles["table"]), Paragraph("Tổng công ty Chăn nuôi Việt Nam - CTCP (Vilico)", styles["table"]), Paragraph("Công ty con trực tiếp", styles["table"]), Paragraph("0100104441", styles["table"]), Paragraph("68.0%", styles["table"])],
        [Paragraph("3", styles["table"]), Paragraph("Công ty TNHH Bò Sữa Việt Nam", styles["table"]), Paragraph("Công ty con (Trang trại bò sữa)", styles["table"]), Paragraph("0309998812", styles["table"]), Paragraph("100.0%", styles["table"])],
        [Paragraph("4", styles["table"]), Paragraph("Driftwood Dairy Holding Corporation", styles["table"]), Paragraph("Công ty con tại Hoa Kỳ", styles["table"]), Paragraph("Mỹ - US95-12345", styles["table"]), Paragraph("100.0%", styles["table"])],
        [Paragraph("5", styles["table"]), Paragraph("Angkor Dairy Products Co., Ltd", styles["table"]), Paragraph("Công ty con tại Campuchia", styles["table"]), Paragraph("KH - Co.654321", styles["table"]), Paragraph("100.0%", styles["table"])],
    ]
    t = Table(table_data, colWidths=[30, 200, 140, 100, 50])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    add_signature_block(elements, styles, "NGƯỜI KÊ KHAI", "Lê Thành Liêm", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_A21(output_path, styles):
    """A.2.1: Bản sao CCCD người đại diện pháp luật"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "05/2023/VNM-PL", "TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023")
    elements.append(Paragraph("BẢN SAO THẺ CĂN CƯỚC CÔNG DÂN<br/>NGƯỜI ĐẠI DIỆN THEO PHÁP LUẬT", styles["title"]))
    content = """
    <b>Họ và tên:</b> <b>MAI KIỀU LIÊN</b><br/>
    <b>Số định danh cá nhân / CCCD:</b> <b>079153001289</b><br/>
    <b>Ngày sinh:</b> 01/09/1953 - <b>Giới tính:</b> Nữ - <b>Quốc tịch:</b> Việt Nam<br/>
    <b>Quê quán:</b> Huyện Vị Thủy, Tỉnh Hậu Giang<br/>
    <b>Nơi thường trú:</b> Phường Bến Nghé, Quận 1, Thành phố Hồ Chí Minh<br/>
    <b>Ngày cấp:</b> 10/05/2021 - <b>Nơi cấp:</b> Cục Cảnh sát Quản lý hành chính về trật tự xã hội<br/>
    <b>Giá trị đến:</b> Không thời hạn (Người trên 60 tuổi theo Luật CCCD)<br/><br/>
    <i>Cam kết của doanh nghiệp: Bản sao căn cước công dân trích xuất đúng với bản chính do Bà Mai Kiều Liên xuất trình để thực hiện thủ tục vay vốn tại Agribank.</i>
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "XÁC NHẬN CỦA TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_B1_01(output_path, styles):
    """B.1_01: Báo cáo tài chính kiểm toán năm 2023 (KPMG kiểm toán)"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    add_official_header(elements, styles, "CÔNG TY TNHH KPMG VIỆT NAM<br/><i>Independent Auditor's Report</i>", "KPMG-2023/VNM-FS", "TP. Hồ Chí Minh, ngày 28 tháng 02 năm 2024")
    elements.append(Paragraph("BÁO CÁO CỦA KIỂM TOÁN VIÊN ĐỘC LẬP<br/>VÀ BÁO CÁO TÀI CHÍNH HỢP NHẤT NĂM 2023<br/><b>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</b>", styles["title"]))

    content = """
    <b>Kính gửi: Các Cổ đông, Hội đồng Quản trị và Ban Tổng Giám đốc Công ty Cổ phần Sữa Việt Nam</b><br/>
    Chúng tôi đã kiểm toán báo cáo tài chính hợp nhất đính kèm của Vinamilk, bao gồm Bảng cân đối kế toán hợp nhất tại ngày 31/12/2023, Báo cáo kết quả hoạt động kinh doanh hợp nhất, Báo cáo lưu chuyển tiền tệ hợp nhất cho năm tài chính kết thúc cùng ngày.<br/>
    <b>Ý kiến của Kiểm toán viên:</b> Theo ý kiến của chúng tôi, BCTC hợp nhất đã phản ánh trung thực và hợp lý, trên các khía cạnh trọng yếu, tình hình tài chính hợp nhất của Vinamilk tại ngày 31/12/2023, cũng như kết quả hoạt động kinh doanh và lưu chuyển tiền tệ cho năm tài chính kết thúc cùng ngày, phù hợp với Chuẩn mực Kế toán Việt Nam (VAS) và chế độ kế toán doanh nghiệp hiện hành.
    """
    elements.append(Paragraph(content, styles["body"]))
    elements.append(Spacer(1, 10))

    # Bảng số liệu P&L và Balance Sheet
    elements.append(Paragraph("<b>BẢNG TỔNG HỢP CÁC CHỈ TIÊU TÀI CHÍNH TRỌNG YẾU (ĐVT: TRIỆU ĐỒNG)</b>", styles["table_h"]))
    table_data = [
        [Paragraph("<b>Mã số</b>", styles["table_h"]), Paragraph("<b>Chỉ tiêu tài chính</b>", styles["table_h"]), Paragraph("<b>Năm 2022</b>", styles["table_h"]), Paragraph("<b>Năm 2023 (Kiểm toán)</b>", styles["table_h"])],
        [Paragraph("10", styles["table"]), Paragraph("Doanh thu thuần bán hàng và CCDV", styles["table"]), Paragraph("59.925.200", styles["table"]), Paragraph("<b>60.374.459</b>", styles["table"])],
        [Paragraph("11", styles["table"]), Paragraph("Giá vốn hàng bán", styles["table"]), Paragraph("36.045.200", styles["table"]), Paragraph("35.789.288", styles["table"])],
        [Paragraph("20", styles["table"]), Paragraph("Lợi nhuận gộp về bán hàng", styles["table"]), Paragraph("23.880.000", styles["table"]), Paragraph("<b>24.585.171</b>", styles["table"])],
        [Paragraph("21", styles["table"]), Paragraph("Doanh thu hoạt động tài chính (lãi tiền gửi)", styles["table"]), Paragraph("1.350.000", styles["table"]), Paragraph("1.688.423", styles["table"])],
        [Paragraph("23", styles["table"]), Paragraph("Chi phí lãi vay ngân hàng", styles["table"]), Paragraph("315.000", styles["table"]), Paragraph("338.500", styles["table"])],
        [Paragraph("50", styles["table"]), Paragraph("Lợi nhuận kế toán trước thuế (LNTT)", styles["table"]), Paragraph("10.496.000", styles["table"]), Paragraph("<b>10.968.188</b>", styles["table"])],
        [Paragraph("60", styles["table"]), Paragraph("LỢI NHUẬN SAU THUẾ TNDN (LNST)", styles["table"]), Paragraph("8.578.000", styles["table"]), Paragraph("<b>9.019.467</b>", styles["table"])],
        [Paragraph("100", styles["table"]), Paragraph("TỔNG TÀI SẢN (Tại 31/12)", styles["table"]), Paragraph("48.482.000", styles["table"]), Paragraph("<b>53.227.487</b>", styles["table"])],
        [Paragraph("110", styles["table"]), Paragraph("- Tiền & Tiền gửi ngân hàng có kỳ hạn", styles["table"]), Paragraph("19.500.000", styles["table"]), Paragraph("23.047.300", styles["table"])],
        [Paragraph("300", styles["table"]), Paragraph("NỢ PHẢI TRẢ", styles["table"]), Paragraph("15.666.000", styles["table"]), Paragraph("<b>17.481.160</b>", styles["table"])],
        [Paragraph("320", styles["table"]), Paragraph("- Vay ngắn hạn ngân hàng tài trợ VLĐ", styles["table"]), Paragraph("4.900.000", styles["table"]), Paragraph("8.440.000", styles["table"])],
        [Paragraph("400", styles["table"]), Paragraph("VỐN CHỦ SỞ HỮU", styles["table"]), Paragraph("32.816.000", styles["table"]), Paragraph("<b>35.746.327</b>", styles["table"])],
        [Paragraph("OCF", styles["table"]), Paragraph("Lưu chuyển tiền thuần từ HĐKD", styles["table"]), Paragraph("+8.900.000", styles["table"]), Paragraph("<b>+9.845.000</b>", styles["table"])],
    ]
    t = Table(table_data, colWidths=[35, 230, 110, 140])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (2,1), (3,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)

    add_signature_block(elements, styles, "CÔNG TY TNHH KPMG VIỆT NAM<br/>KIỂM TOÁN VIÊN ĐỘC LẬP", "Trần Đình Hậu", "TỔNG GIÁM ĐỐC VINAMILK", "Mai Kiều Liên", STAMP_KPMG, SIG_AUDITOR)
    doc.build(elements)


def create_doc_B3(output_path, styles):
    """B.3: Bảng kê chi tiết các khoản phải thu và tồn kho lớn"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "08/2023/VNM-TC", "TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023")
    elements.append(Paragraph("BẢNG KÊ CHI TIẾT CÁC KHOẢN PHẢI THU VÀ HÀNG TỒN KHO<br/><i>(Chiếm trên 10% Tổng tài sản theo BCTC kiểm toán 2023)</i>", styles["title"]))

    content = """
    <b>1. Phải thu ngắn hạn khách hàng lớn (Tổng: 6.133 tỷ VNĐ):</b><br/>
    - Chuỗi Saigon Co.op (Liên hiệp HTX TM TP.HCM): 1.250 tỷ VNĐ (Kỳ hạn thanh toán 30-45 ngày, nợ nhóm 1).<br/>
    - Chuỗi WinCommerce (WinMart / WinMart+): 880 tỷ VNĐ (Kỳ hạn thanh toán 30 ngày, đúng hạn).<br/>
    - Chuỗi Bách Hóa Xanh (MWG): 720 tỷ VNĐ (Đúng hạn thanh toán).<br/>
    - Khách hàng xuất khẩu Trung Đông (Dubai, Iraq): 950 tỷ VNĐ (Thanh toán qua L/C không hủy ngang).<br/><br/>
    <b>2. Hàng tồn kho phục vụ sản xuất (Tổng: 5.618 tỷ VNĐ):</b><br/>
    - Nguyên liệu sữa bột nguyên kem, sữa gầy nhập khẩu (Fonterra, Fonterra New Zealand): 2.850 tỷ VNĐ.<br/>
    - Bao bì đóng gói tiệt trùng tiệt trùng (Tetra Pak Thụy Điển): 920 tỷ VNĐ.<br/>
    - Thành phẩm sữa tươi, sữa chua, sữa đặc, sữa bột lưu kho phân phối: 1.848 tỷ VNĐ.<br/>
    <i>Đánh giá: Hàng tồn kho luân chuyển nhanh (vòng quay ~6.4 vòng/năm), không có hàng tồn ứ đọng suy giảm giá trị.</i>
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "KẾ TOÁN TRƯỞNG", "Lê Thành Liêm", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_CI11(output_path, styles):
    """C.I.1.1: Phương án sử dụng vốn lưu động năm 2023-2024"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN<br/>SỮA VIỆT NAM", "12/2023/VNM-PA", "TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023")
    elements.append(Paragraph("PHƯƠNG ÁN SẢN XUẤT KINH DOANH VÀ SỬ DỤNG VỐN VAY<br/>HẠN MỨC VỐN LƯU ĐỘNG NĂM 2023 - 2024", styles["title"]))

    content = """
    <b>Kính gửi: NGÂN HÀNG NÔNG NGHIỆP VÀ PHÁT TRIỂN NÔNG THÔN VIỆT NAM (AGRIBANK)<br/>CHI NHÁNH THÀNH PHỐ HỒ CHÍ MINH</b><br/><br/>
    <b>1. Nhu cầu vốn lưu động năm kế hoạch:</b><br/>
    - Kế hoạch doanh thu thuần năm 2023-2024: <b>62.000 tỷ VNĐ</b>.<br/>
    - Giá vốn hàng bán dự kiến: <b>36.800 tỷ VNĐ</b>.<br/>
    - Vòng quay vốn lưu động: <b>5.5 vòng/năm</b>.<br/>
    - Tổng nhu cầu vốn lưu động bình quân: <b>6.690 tỷ VNĐ</b>.<br/>
    - Vốn tự có và vốn chiếm dụng hợp pháp tham gia (60%): <b>4.014 tỷ VNĐ</b>.<br/>
    - <b>Nhu cầu vay vốn lưu động ngân hàng (40%):</b> <b>2.676 tỷ - 3.000 tỷ VNĐ</b>.<br/><br/>
    <b>2. Đề xuất cấp tín dụng tại Agribank:</b><br/>
    - Hạn mức tín dụng đề nghị: <b>3.000.000.000.000 VNĐ</b> (Ba nghìn tỷ đồng).<br/>
    - Thời hạn duy trì hạn mức: <b>12 tháng</b>. Thời hạn mỗi khế ước nhận nợ tối đa: <b>06 tháng</b>.<br/>
    - Mục đích: Thu mua sữa tươi nguyên liệu từ nông hộ, hợp tác xã và các trang trại bò sữa sinh thái; nhập khẩu nguyên liệu bột sữa chất lượng cao phục vụ chế biến.<br/>
    - Biện pháp bảo đảm: Thế chấp Nhà máy Sữa Bình Dương (định giá 4.200 tỷ VNĐ) và phong tỏa tiền gửi có kỳ hạn (1.500 tỷ VNĐ).<br/>
    - Nguồn trả nợ: Doanh thu bán hàng từ mạng lưới phân phối hơn 200.000 điểm bán lẻ và hệ thống siêu thị toàn quốc.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "KẾ TOÁN TRƯỞNG", "Lê Thành Liêm", "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", STAMP_VNM, SIG_MKL)
    doc.build(elements)


def create_doc_CI12(output_path, styles):
    """C.I.1.2: Nghị quyết HĐQT Vinamilk phê duyệt vay vốn Agribank"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "HỘI ĐỒNG QUẢN TRỊ<br/>CTCP SỮA VIỆT NAM", "12/NQ-CTS.HĐQT/2023", "TP. Hồ Chí Minh, ngày 10 tháng 04 năm 2023")
    elements.append(Paragraph("NGHỊ QUYẾT HỘI ĐỒNG QUẢN TRỊ<br/>V/v: Phê duyệt vay vốn hạn mức và thế chấp tài sản tại Agribank", styles["title"]))

    content = """
    <b>HỘI ĐỒNG QUẢN TRỊ CÔNG TY CỔ PHẦN SỮA VIỆT NAM</b><br/>
    - Căn cứ Điều lệ Công ty Cổ phần Sữa Việt Nam;<br/>
    - Căn cứ Phương án sản xuất kinh doanh sữa năm 2023-2024 do Tổng Giám đốc trình.<br/><br/>
    <b>QUYẾT NGHỊ:</b><br/>
    <b>Điều 1:</b> Thông qua việc vay vốn theo hạn mức tín dụng tại <b>Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam - Chi nhánh TP. Hồ Chí Minh</b> với các điều kiện sau:<br/>
    - Hạn mức tín dụng: <b>3.000.000.000.000 VNĐ</b> (Ba nghìn tỷ đồng).<br/>
    - Thời hạn duy trì hạn mức: 12 tháng.<br/>
    - Mục đích vay: Bổ sung vốn lưu động sản xuất kinh doanh.<br/>
    <b>Điều 2:</b> Thông qua việc sử dụng tài sản thuộc quyền sở hữu của Vinamilk để thế chấp bảo đảm cho khoản vay nêu trên, bao gồm: Toàn bộ công trình xây dựng và máy móc thiết bị tại <b>Nhà máy Sữa Việt Nam (Mega Market Bình Dương)</b> và Hợp đồng tiền gửi tại Agribank.<br/>
    <b>Điều 3:</b> Giao Bà <b>MAI KIỀU LIÊN</b> - Tổng Giám đốc đại diện Vinamilk đàm phán, ký kết Hợp đồng tín dụng, Hợp đồng thế chấp tài sản, Khế ước nhận nợ và các văn kiện tín dụng liên quan với Agribank.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TM. HỘI ĐỒNG QUẢN TRỊ<br/>CHỦ TỊCH", "Nguyễn Hạnh Phúc", STAMP_VNM, SIG_NHP)
    doc.build(elements)


def create_doc_D1(output_path, styles):
    """D.1: Giấy chứng nhận QSD đất & sở hữu công trình Nhà máy Sữa Bình Dương"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "UBND TỈNH BÌNH DƯƠNG<br/>SỞ TÀI NGUYÊN VÀ MÔI TRƯỜNG", "BB 987654/GCN", "Bình Dương, ngày 15 tháng 06 năm 2012")
    elements.append(Paragraph("GIẤY CHỨNG NHẬN<br/>QUYỀN SỬ DỤNG ĐẤT, QUYỀN SỞ HỮU NHÀ Ở VÀ TÀI SẢN KHÁC GẮN LIỀN VỚI ĐẤT", styles["title"]))

    content = """
    <b>I. Người sử dụng đất, chủ sở hữu nhà ở và tài sản khác gắn liền với đất:</b><br/>
    <b>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</b><br/>
    - Mã số doanh nghiệp: 0300588569.<br/>
    - Trụ sở: Số 10 Tân Trào, Phường Tân Phú, Quận 7, TP. Hồ Chí Minh.<br/><br/>
    <b>II. Thửa đất, nhà ở và tài sản khác gắn liền với đất:</b><br/>
    <b>1. Thửa đất:</b><br/>
    - Thửa đất số: 128 - Tờ bản đồ số: 45.<br/>
    - Địa chỉ: Lô CN6, Đường D1, Khu công nghiệp Mỹ Phước 2, Thị xã Bến Cát, Tỉnh Bình Dương.<br/>
    - Diện tích: <b>200.000 m²</b> (Hai mươi héc-ta).<br/>
    - Mục đích sử dụng: Đất khu công nghiệp (Xây dựng Nhà máy chế biến sữa công nghệ cao).<br/>
    - Thời hạn sử dụng: Đến ngày 30/06/2055. Nguồn gốc: Nhà nước cho thuê đất trả tiền một lần.<br/><br/>
    <b>2. Tài sản gắn liền với đất:</b><br/>
    - Tên công trình: <b>Nhà máy Sữa Việt Nam (Mega Market Bình Dương)</b>.<br/>
    - Diện tích xây dựng: 120.000 m²; Diện tích sàn: 150.000 m².<br/>
    - Kết cấu: Khung thép tiền chế chịu lực, sàn bê tông cốt thép, hệ thống kho thông minh tự động hoàn toàn.<br/>
    - Công suất thiết kế: 800 triệu lít sữa/năm (Nhà máy sữa lớn nhất Đông Nam Á).
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TM. ỦY BAN NHÂN DÂN TỈNH BÌNH DƯƠNG<br/>GIÁM ĐỐC SỞ TN&MT", "Trần Thanh Liêm", STAMP_GOV, SIG_NHP)
    doc.build(elements)


def create_doc_D5(output_path, styles):
    """D.5: Giấy chứng nhận bảo hiểm tài sản Nhà máy Sữa Mega Market"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "TỔNG CÔNG TY CỔ PHẦN<br/>BẢO HIỂM PETROLIMEX (PJICO)", "PJ-2023/VNM-01", "TP. Hồ Chí Minh, ngày 01 tháng 01 năm 2023")
    elements.append(Paragraph("GIẤY CHỨNG NHẬN BẢO HIỂM MỌI RỦI RO TÀI SẢN<br/>VÀ GIÁN ĐOẠN KINH DOANH", styles["title"]))

    content = """
    <b>Người được bảo hiểm:</b> CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)<br/>
    <b>Địa điểm được bảo hiểm:</b> Nhà máy Sữa Việt Nam - Lô CN6, KCN Mỹ Phước 2, Bến Cát, Bình Dương.<br/>
    <b>Thời hạn bảo hiểm:</b> Từ 00h00 ngày 01/01/2023 đến 24h00 ngày 31/12/2023.<br/><br/>
    <b>TỔNG SỐ TIỀN BẢO HIỂM:</b> <b>4.500.000.000.000 VNĐ</b> (Bốn nghìn năm trăm tỷ đồng).<br/>
    - Mục 1: Nhà xưởng, công trình kiến trúc và kho tự động: 1.800.000.000.000 VNĐ.<br/>
    - Mục 2: Máy móc thiết bị và dây chuyền chế biến sữa Tetra Pak: 2.200.000.000.000 VNĐ.<br/>
    - Mục 3: Nguyên vật liệu và thành phẩm lưu kho: 500.000.000.000 VNĐ.<br/><br/>
    <b>ĐIỀU KHOẢN CHUYỂN QUYỀN THỤ HƯỞNG BẢO HIỂM:</b><br/>
    PJICO xác nhận <b>NGÂN HÀNG NÔNG NGHIỆP VÀ PHÁT TRIỂN NÔNG THÔN VIỆT NAM - CHI NHÁNH TP. HỒ CHÍ MINH</b> là <b>Bên thụ hưởng bảo hiểm thứ nhất duy nhất và không thể hủy ngang</b> đối với mọi bồi thường bảo hiểm phát sinh theo hợp đồng bảo hiểm này để bảo đảm cho nghĩa vụ nợ vay của Vinamilk.
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "", "", "TỔNG CÔNG TY CP BẢO HIỂM PETROLIMEX<br/>GIÁM ĐỐC CHI NHÁNH", "Đoàn Kiên Cường", STAMP_AGRI, SIG_AUDITOR)
    doc.build(elements)


def create_doc_D6(output_path, styles):
    """D.6: Chứng thư thẩm định giá độc lập VinaControl số 128/CT-TĐG"""
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    elements = []
    add_official_header(elements, styles, "CÔNG TY CỔ PHẦN THẨM ĐỊNH GIÁ<br/>VINACONTROL", "128/CT-TĐG/2023", "TP. Hồ Chí Minh, ngày 20 tháng 03 năm 2023")
    elements.append(Paragraph("CHỨNG THƯ THẨM ĐỊNH GIÁ TÀI SẢN<br/>Mục đích: Xác định giá trị TSBĐ vay vốn tại Agribank", styles["title"]))

    content = """
    <b>1. Khách hàng yêu cầu thẩm định:</b> Agribank Chi nhánh TP.HCM & Công ty Cổ phần Sữa Việt Nam.<br/>
    <b>2. Tài sản thẩm định:</b> Toàn bộ quyền sử dụng 200.000 m² đất thuê trả tiền một lần và Công trình xây dựng, Dây chuyền thiết bị chế biến sữa tại Nhà máy Sữa Mega Market Bình Dương.<br/>
    <b>3. Thời điểm thẩm định giá:</b> Tháng 03/2023.<br/>
    <b>4. Cơ sở thẩm định:</b> Tiêu chuẩn Thẩm định giá Việt Nam số 01, 02, 03, 08, 09, 10 do Bộ Tài chính ban hành.<br/>
    <b>5. Phương pháp thẩm định:</b> Phương pháp chi phí thay thế kết hợp Phương pháp so sánh thị trường.<br/><br/>
    <b>KẾT QUẢ THẨM ĐỊNH GIÁ TÀI SẢN:</b><br/>
    - Giá trị Quyền sử dụng 200.000 m² đất công nghiệp: <b>1.200.000.000.000 VNĐ</b>.<br/>
    - Giá trị Công trình xây dựng nhà xưởng và kho tự động: <b>1.150.000.000.000 VNĐ</b>.<br/>
    - Giá trị Máy móc thiết bị, dây chuyền chế biến sữa Tetra Pak: <b>1.850.000.000.000 VNĐ</b>.<br/>
    - <b>TỔNG GIÁ TRỊ TÀI SẢN THẨM ĐỊNH:</b> <b style="color:#ae1c3f;">4.200.000.000.000 VNĐ</b><br/>
    <i>(Bằng chữ: Bốn nghìn hai trăm tỷ đồng).</i>
    """
    elements.append(Paragraph(content, styles["body"]))
    add_signature_block(elements, styles, "THẨM ĐỊNH VIÊN VỀ GIÁ", "Nguyễn Văn Dũng", "TỔNG GIÁM ĐỐC VINACONTROL", "Trần Quốc Thái", STAMP_KPMG, SIG_AUDITOR)
    doc.build(elements)


# ==============================================================================
# 5. CHƯƠNG TRÌNH CHÍNH (MAIN ORCHESTRATION)
# ==============================================================================

def main():
    styles = get_styles()

    folders = {
        "A": os.path.join(OUTPUT_BASE, "A_Ho_So_Phap_Ly"),
        "B": os.path.join(OUTPUT_BASE, "B_Ho_So_Kinh_Te"),
        "C": os.path.join(OUTPUT_BASE, "C_Ho_So_Vay_Von"),
        "D": os.path.join(OUTPUT_BASE, "D_Ho_So_Tai_San_Bao_Dam"),
    }
    for f in folders.values():
        os.makedirs(f, exist_ok=True)

    print(">>> BẮT ĐẦU SINH BỘ HỒ SƠ TÍN DỤNG PHÁP NHÂN VINAMILK (PDF SCANNED)...")

    # Nhóm A
    print("1. Đang sinh Nhóm A (Hồ sơ pháp lý)...")
    create_doc_A11(os.path.join(folders["A"], "790000123DN0300588569_A11_01.pdf"), styles)
    create_doc_A14(os.path.join(folders["A"], "790000123DN0300588569_A14_01.pdf"), styles)
    create_doc_A15(os.path.join(folders["A"], "790000123DN0300588569_A15_01.pdf"), styles)
    create_doc_A16(os.path.join(folders["A"], "790000123DN0300588569_A16_01.pdf"), styles)
    create_doc_A18(os.path.join(folders["A"], "790000123DN0300588569_A18_01.pdf"), styles)
    create_doc_A19(os.path.join(folders["A"], "790000123DN0300588569_A19_01.pdf"), styles)
    create_doc_A21(os.path.join(folders["A"], "790000123DN0300588569_A21_01.pdf"), styles)

    # Nhóm B
    print("2. Đang sinh Nhóm B (Hồ sơ kinh tế BCTC KPMG)...")
    create_doc_B1_01(os.path.join(folders["B"], "790000123DN0300588569_B1_01.pdf"), styles)
    create_doc_B3(os.path.join(folders["B"], "790000123DN0300588569_B3_01.pdf"), styles)

    # Nhóm C
    print("3. Đang sinh Nhóm C (Phương án vay vốn & Nghị quyết HĐQT)...")
    create_doc_CI11(os.path.join(folders["C"], "790000123DN0300588569_CI11_01.pdf"), styles)
    create_doc_CI12(os.path.join(folders["C"], "790000123DN0300588569_CI12_01.pdf"), styles)

    # Nhóm D
    print("4. Đang sinh Nhóm D (Tài sản bảo đảm & Định giá)...")
    create_doc_D1(os.path.join(folders["D"], "790000123DN0300588569_D1_01.pdf"), styles)
    create_doc_D5(os.path.join(folders["D"], "790000123DN0300588569_D5_01.pdf"), styles)
    create_doc_D6(os.path.join(folders["D"], "790000123DN0300588569_D6_01.pdf"), styles)

    print(f">>> HOÀN TẤT SINH BỘ HỒ SƠ TÍN DỤNG TẠI: {OUTPUT_BASE}")


if __name__ == "__main__":
    main()
