# -*- coding: utf-8 -*-
"""
generate_remaining_dossier.py
Sinh các tài liệu còn lại cho bộ hồ sơ tín dụng Vinamilk (B, C, D, E, F, G, H, I) dạng PDF Scanned
hoàn chỉnh 100% tài liệu theo chuẩn SDTN.
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

# 1. Đăng ký Font chữ tiếng Việt macOS
BASE_FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Times", f"{BASE_FONT_DIR}/Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("Times-Bold", f"{BASE_FONT_DIR}/Times New Roman Bold.ttf"))
pdfmetrics.registerFont(TTFont("Times-Italic", f"{BASE_FONT_DIR}/Times New Roman Italic.ttf"))
pdfmetrics.registerFont(TTFont("Times-BoldItalic", f"{BASE_FONT_DIR}/Times New Roman Bold Italic.ttf"))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_BASE = os.path.join(PROJECT_ROOT, "documents", "7900.001.23.DN.0300588569")
TEMP_DIR = os.path.join(PROJECT_ROOT, "temp_stamps")
os.makedirs(TEMP_DIR, exist_ok=True)

# 2. Con dấu bổ sung
STAMP_VNM = os.path.join(TEMP_DIR, "stamp_vnm.png")
STAMP_AGRI_CN = os.path.join(TEMP_DIR, "stamp_agri_cn.png")
STAMP_AGRI_TTPD = os.path.join(TEMP_DIR, "stamp_agri_ttpd.png")
STAMP_CIC = os.path.join(TEMP_DIR, "stamp_cic.png")
STAMP_KPMG = os.path.join(TEMP_DIR, "stamp_kpmg.png")

SIG_MKL = os.path.join(TEMP_DIR, "sig_mkl.png")
SIG_LTL = os.path.join(TEMP_DIR, "sig_ltl.png")
SIG_NHP = os.path.join(TEMP_DIR, "sig_nhp.png")
SIG_NHM = os.path.join(TEMP_DIR, "sig_nhm.png")
SIG_TTP = os.path.join(TEMP_DIR, "sig_ttp.png")
SIG_LVH = os.path.join(TEMP_DIR, "sig_lvh.png")
SIG_PQT = os.path.join(TEMP_DIR, "sig_pqt.png")
SIG_VDT = os.path.join(TEMP_DIR, "sig_vdt.png")
SIG_DQV = os.path.join(TEMP_DIR, "sig_dqv.png")
SIG_MA = os.path.join(TEMP_DIR, "sig_ma.png")

create_circular_stamp("CÔNG TY CỔ PHẦN SỮA VIỆT NAM", "VINAMILK", "MST: 0300588569").save(STAMP_VNM)
create_circular_stamp("NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VIỆT NAM", "AGRIBANK", "CN TP. HỒ CHÍ MINH").save(STAMP_AGRI_CN)
create_circular_stamp("NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VIỆT NAM", "AGRIBANK", "TTPD MIỀN NAM").save(STAMP_AGRI_TTPD)
create_circular_stamp("NGÂN HÀNG NHÀ NƯỚC VIỆT NAM", "CIC", "TT THÔNG TIN TÍN DỤNG").save(STAMP_CIC)
create_circular_stamp("CÔNG TY TNHH KPMG VIỆT NAM", "KPMG", "KIỂM TOÁN VIÊN").save(STAMP_KPMG)

create_signature_image("Mai Kiều Liên").save(SIG_MKL)
create_signature_image("Lê Thành Liêm").save(SIG_LTL)
create_signature_image("Nguyễn Hạnh Phúc").save(SIG_NHP)
create_signature_image("Nguyễn Hoàng Minh").save(SIG_NHM)
create_signature_image("Trần Thanh Phong").save(SIG_TTP)
create_signature_image("Lê Văn Hùng").save(SIG_LVH)
create_signature_image("Phạm Quốc Tuấn").save(SIG_PQT)
create_signature_image("Vũ Đình Trọng").save(SIG_VDT)
create_signature_image("Đỗ Quang Vinh").save(SIG_DQV)
create_signature_image("Nguyễn Thị Mai Anh").save(SIG_MA)


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
        fontSize=12.5,
        leading=16,
        alignment=1,
        spaceAfter=10
    )

    header_left = ParagraphStyle(
        "HeaderLeft",
        parent=normal,
        fontName="Times-Bold",
        fontSize=9,
        leading=12,
        alignment=0
    )

    header_right = ParagraphStyle(
        "HeaderRight",
        parent=normal,
        fontName="Times-Bold",
        fontSize=9,
        leading=12,
        alignment=1
    )

    body_text = ParagraphStyle(
        "BodyTextVN",
        parent=normal,
        fontSize=9.5,
        leading=14,
        alignment=4
    )

    bold_text = ParagraphStyle(
        "BoldTextVN",
        parent=body_text,
        fontName="Times-Bold"
    )

    return normal, title_style, header_left, header_right, body_text, bold_text


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(36, 25, "Hồ sơ tín dụng VNM - Agribank SDTN | Mã HS: 7900.001.23.DN.0300588569")
        page_str = f"Trang {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 36, 25, page_str)
        self.restoreState()


def make_doc(folder_name, filename):
    folder = os.path.join(OUTPUT_BASE, folder_name)
    os.makedirs(folder, exist_ok=True)
    pdf_path = os.path.join(folder, filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=40
    )
    return doc


def build_doc(doc, story):
    doc.build(story, canvasmaker=NumberedCanvas)


def add_header(story, left_title, left_sub, right_title, right_sub, doc_date="TP. Hồ Chí Minh, ngày 18 tháng 04 năm 2023"):
    _, _, h_left, h_right, _, _ = get_styles()
    t_left = [
        Paragraph(left_title, h_left),
        Paragraph(left_sub, ParagraphStyle("HSubL", parent=h_left, fontName="Times-Italic", fontSize=8.5, leading=11))
    ]
    t_right = [
        Paragraph(right_title, h_right),
        Paragraph(right_sub, ParagraphStyle("HSubR", parent=h_right, fontName="Times-Bold", fontSize=8.5, leading=11)),
        Spacer(1, 2),
        Paragraph(f"<i>{doc_date}</i>", ParagraphStyle("Date", parent=h_right, fontName="Times-Italic", fontSize=8, leading=10))
    ]
    header_table = Table([[t_left, t_right]], colWidths=[240, 275])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))


def add_dual_signatures(story, title1, name1, sig_img1, title2, name2, sig_img2, stamp_img2=None):
    normal, _, _, _, _, _ = get_styles()
    col1 = [
        Paragraph(f"<strong>{title1}</strong>", ParagraphStyle("S1", parent=normal, alignment=1, fontName="Times-Bold", fontSize=9.5)),
        Spacer(1, 4),
        RLImage(sig_img1, width=100, height=45) if sig_img1 else Spacer(1, 45),
        Paragraph(f"<strong>{name1}</strong>", ParagraphStyle("N1", parent=normal, alignment=1, fontName="Times-Bold", fontSize=9.5))
    ]
    col2 = [
        Paragraph(f"<strong>{title2}</strong>", ParagraphStyle("S2", parent=normal, alignment=1, fontName="Times-Bold", fontSize=9.5)),
        Spacer(1, 4),
        RLImage(sig_img2, width=100, height=45) if sig_img2 else Spacer(1, 45),
        Paragraph(f"<strong>{name2}</strong>", ParagraphStyle("N2", parent=normal, alignment=1, fontName="Times-Bold", fontSize=9.5))
    ]
    if stamp_img2:
        col2.insert(2, RLImage(stamp_img2, width=75, height=75))

    sig_table = Table([[col1, col2]], colWidths=[255, 260])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(KeepTogether(sig_table))


# ==============================================================================
# 1. A.1.2 - Điều lệ Vinamilk (Trích lục)
# ==============================================================================
def gen_A12():
    doc = make_doc("A_Ho_So_Phap_Ly", "790000123DN0300588569_A12_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "CÔNG TY CP SỮA VIỆT NAM<br/>HỘI ĐỒNG QUẢN TRỊ", "Số: 01/2022/ĐL-VNM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 26 tháng 04 năm 2022")
    story.append(Paragraph("ĐIỀU LỆ TỔ CHỨC VÀ HOẠT ĐỘNG<br/>(TRÍCH LỤC THẨM QUYỀN VAY VỐN & ĐẠI DIỆN PHÁP LUẬT)", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Điều 1: Tên doanh nghiệp:</b> CÔNG TY CỔ PHẦN SỮA VIỆT NAM (Tên viết tắt: VINAMILK).", body_text))
    story.append(Paragraph("<b>Điều 2: Vốn điều lệ:</b> 20.899.554.450.000 đồng (Hai mươi nghìn tám trăm chín mươi chín tỷ năm trăm năm mươi bốn triệu bốn trăm năm mươi nghìn đồng).", body_text))
    story.append(Paragraph("<b>Điều 35: Người đại diện theo pháp luật:</b> Tổng Giám đốc là Người đại diện theo pháp luật của Công ty. Tổng Giám đốc đại diện cho Công ty ký kết các hợp đồng kinh tế, hợp đồng tín dụng, hợp đồng thế chấp tài sản phục vụ hoạt động sản xuất kinh doanh phù hợp với Nghị quyết của Đại hội đồng Cổ đông và Hội đồng Quản trị.", body_text))
    story.append(Paragraph("<b>Điều 42: Thẩm quyền vay vốn và cam kết tín dụng:</b>", bold_text))
    story.append(Paragraph("- Hội đồng Quản trị có thẩm quyền phê duyệt các khoản vay vốn ngân hàng, phát hành trái phiếu và các giao dịch tài chính có giá trị trong hạn mức được ĐHĐCĐ ủy quyền.", body_text))
    story.append(Paragraph("- Tổng Giám đốc căn cứ Nghị quyết HĐQT trực tiếp ký kết Hợp đồng tín dụng, khế ước nhận nợ và sử dụng con dấu của Công ty.", body_text))
    story.append(Spacer(1, 25))
    add_dual_signatures(story, "CHỦ TỊCH HỘI ĐỒNG QUẢN TRỊ", "Nguyễn Hạnh Phúc", SIG_NHP, "TỔNG GIÁM ĐỐC / ĐẠI DIỆN PHÁP LUẬT", "Mai Kiều Liên", SIG_MKL, STAMP_VNM)
    build_doc(doc, story)
    print("✓ Đã sinh A12_01.pdf")


# ==============================================================================
# 2. B.1_2022 & B.2 - BCTC 2022 và BCTC Q4
# ==============================================================================
def gen_B1_2022():
    doc = make_doc("B_Ho_So_Kinh_Te", "790000123DN0300588569_B1_02.pdf")
    normal, title_style, _, _, body_text, _ = get_styles()
    story = []
    add_header(story, "CÔNG TY TNHH KPMG VIỆT NAM", "Số: 22-01-00215/BCKT",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 28 tháng 03 năm 2023")
    story.append(Paragraph("BÁO CÁO CỦA KIỂM TOÁN VIÊN ĐỘC LẬP<br/>VỀ BÁO CÁO TÀI CHÍNH HỢP NHẤT NĂM 2022 CỦA VINAMILK", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Ý kiến của Kiểm toán viên:</b> Theo ý kiến của chúng tôi, Báo cáo tài chính hợp nhất đã phản ánh trung thực và hợp lý, trên các khía cạnh trọng yếu, tình hình tài chính hợp nhất của Công ty Cổ phần Sữa Việt Nam tại ngày 31/12/2022, cũng như kết quả hoạt động kinh doanh hợp nhất và lưu chuyển tiền tệ cho năm tài chính kết thúc cùng ngày.", body_text))
    story.append(Spacer(1, 8))
    tbl_data = [
        ["Chỉ tiêu chính năm 2022 (VND)", "Hợp nhất 2022"],
        ["Tổng Tài sản", "48.482.576.812.350"],
        ["Vốn chủ sở hữu", "32.836.471.189.120"],
        ["Doanh thu thuần", "59.925.321.415.600"],
        ["Lợi nhuận gộp", "23.887.412.000.000"],
        ["Lợi nhuận sau thuế", "8.577.589.123.400"]
    ]
    t = Table(tbl_data, colWidths=[310, 205])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ae1c3f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('FONTNAME', (0,1), (-1,-1), 'Times'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "KIỂM TOÁN VIÊN HÀNH NGHỀ", "Trần Đình Hậu", SIG_LTL, "TỔNG GIÁM ĐỐC KPMG VIỆT NAM", "Warrick Cleine", SIG_MKL, STAMP_KPMG)
    build_doc(doc, story)
    print("✓ Đã sinh B1_02.pdf")


def gen_B2():
    doc = make_doc("B_Ho_So_Kinh_Te", "790000123DN0300588569_B2_01.pdf")
    _, title_style, _, _, body_text, _ = get_styles()
    story = []
    add_header(story, "CÔNG TY CP SỮA VIỆT NAM<br/>PHÒNG TÀI CHÍNH KẾ TOÁN", "Số: 45/2023/BCTC-VNM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 15 tháng 01 năm 2024")
    story.append(Paragraph("BÁO CÁO TÀI CHÍNH HỢP NHẤT QUÝ 4/2023<br/>(BẢNG CÂN ĐỐI KẾ TOÁN VÀ KẾT QUẢ KINH DOANH TỔNG HỢP)", title_style))
    story.append(Spacer(1, 6))
    tbl_data = [
        ["Chỉ tiêu Quý 4/2023 (triệu VND)", "Quý 4/2023", "Lũy kế cả năm 2023"],
        ["Doanh thu thuần", "15.619.450", "60.374.459"],
        ["Lợi nhuận gộp", "6.420.100", "24.577.100"],
        ["Lợi nhuận sau thuế", "2.350.200", "9.019.467"],
        ["Tiền và tương đương tiền cuối kỳ", "2.618.300", "2.618.300"],
        ["Tổng Tài sản ngắn hạn", "35.811.000", "35.811.000"]
    ]
    t = Table(tbl_data, colWidths=[240, 135, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ae1c3f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,1), (-1,-1), 'Times'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "KẾ TOÁN TRƯỞNG", "Lê Thành Liêm", SIG_LTL, "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", SIG_MKL, STAMP_VNM)
    build_doc(doc, story)
    print("✓ Đã sinh B2_01.pdf")


# ==============================================================================
# 3. C.I.1.3 & D.3
# ==============================================================================
def gen_CI13():
    doc = make_doc("C_Ho_So_Vay_Von", "790000123DN0300588569_CI13_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "CÔNG TY CP SỮA VIỆT NAM<br/>KHỐI CUNG ỨNG & MUA HÀNG", "HĐNT: 88/2023/VNM-TETRA",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 10 tháng 01 năm 2023")
    story.append(Paragraph("HỢP ĐỒNG NGUYÊN TẮC MUA BÁN NGUYÊN PHỤ LIỆU BAO BÌ<br/>VÀ THỎA THUẬN TIÊU THỤ SẢN PHẨM SỮA NĂM 2023 - 2024", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Bên A (Bên Mua):</b> CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK) - Đại diện: Bà Mai Kiều Liên - Tổng Giám đốc.", body_text))
    story.append(Paragraph("<b>Bên B (Bên Cung ứng):</b> CÔNG TY TNHH TETRA PAK VIỆT NAM - Đại diện: Ông Eliseo Barcas - Tổng Giám đốc.", body_text))
    story.append(Paragraph("<b>Nội dung thỏa thuận:</b>", bold_text))
    story.append(Paragraph("1. Bên B cam kết cung ứng định kỳ các loại vật liệu bao bì tiệt trùng phức hợp (Tetra Brik Aseptic) cho toàn bộ 13 nhà máy của Bên A với giá trị dự kiến: <b>2.500.000.000.000 VND/năm</b>.", body_text))
    story.append(Paragraph("2. Hình thức thanh toán: Mở L/C hoặc chuyển tiền T/T qua tài khoản thanh toán của Bên A tại <b>Ngân hàng Agribank Chi nhánh TP.HCM</b>.", body_text))
    story.append(Paragraph("3. Điều khoản đảm bảo: Đảm bảo nguồn hàng ổn định, duy trì tồn kho an toàn tối thiểu 30 ngày sản xuất.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "ĐẠI DIỆN BÊN B (TETRA PAK)", "Eliseo Barcas", SIG_LTL, "ĐẠI DIỆN BÊN A (VINAMILK)", "Mai Kiều Liên", SIG_MKL, STAMP_VNM)
    build_doc(doc, story)
    print("✓ Đã sinh CI13_01.pdf")


def gen_D3():
    doc = make_doc("D_Ho_So_Tai_San_Bao_Dam", "790000123DN0300588569_D3_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>TỔ THẨM ĐỊNH TÀI SẢN BẢO ĐẢM", "Số: 142/BC-TĐTS-NHNo.HCM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 16 tháng 04 năm 2023")
    story.append(Paragraph("BÁO CÁO KẾT QUẢ THẨM ĐỊNH TÀI SẢN BẢO ĐẢM<br/>(NHÀ MÁY SỮA VIỆT NAM - MEGA MARKET BẾN CÁT)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Khách hàng vay vốn:</b> CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK).", body_text))
    story.append(Paragraph("<b>2. Tài sản thẩm định:</b> Quyền sử dụng đất thuê 200.000 m2 (đến năm 2056) và toàn bộ Nhà máy sữa Việt Nam (Mega Market) cùng dây chuyền công nghệ tự động hóa Tetra Pak tại KCN Mỹ Phước 2, TX. Bến Cát, Bình Dương.", body_text))
    story.append(Paragraph("<b>3. Kết quả thẩm định giá trị của Tổ thẩm định Chi nhánh:</b>", bold_text))
    story.append(Paragraph("- Giá trị Quyền sử dụng đất & Công trình xây dựng: <b>1.850.000.000.000 VND</b>", body_text))
    story.append(Paragraph("- Giá trị Máy móc thiết bị, dây chuyền sản xuất: <b>2.350.000.000.000 VND</b>", body_text))
    story.append(Paragraph("- <b>Tổng giá trị TSBĐ xác định: 4.200.000.000.000 VND</b> (Bốn nghìn hai trăm tỷ đồng). Khớp đúng 100% với Chứng thư thẩm định giá số 128/CT-TĐG của Vinacontrol.", bold_text))
    story.append(Paragraph("<b>4. Tỷ lệ cấp tín dụng tối đa (LTV):</b> Đề xuất 71.4% (Tương ứng hạn mức 3.000 tỷ VND / Giá trị định giá 4.200 tỷ VND). Đáp ứng quy định nội bộ Agribank.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "TỔ TRƯỞNG TỔ THẨM ĐỊNH TSBĐ", "Lê Văn Hùng", SIG_LVH, "GIÁM ĐỐC CHI NHÁNH", "Nguyễn Hoàng Minh", SIG_NHM, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh D3_01.pdf")


# ==============================================================================
# 4. Nhóm E: Hồ sơ Chi nhánh lập (E.1.1, E.2, E.3, E.4, E.5)
# ==============================================================================
def gen_E11():
    doc = make_doc("E_Ho_So_Chi_Nhanh_Lap", "790000123DN0300588569_E11_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "NGÂN HÀNG NHÀ NƯỚC VIỆT NAM<br/>TRUNG TÂM THÔNG TIN TÍN DỤNG (CIC)", "Mã tra cứu: CIC-VNM-20230415",
               "BẢN IN TRA CỨU THÔNG TIN KHÁCH HÀNG VAY", "DÀNH CHO TỔ CHỨC TÍN DỤNG", "Hà Nội, ngày 15 tháng 04 năm 2023")
    story.append(Paragraph("BÁO CÁO THÔNG TIN QUAN HỆ TÍN DỤNG DOANH NGHIỆP<br/>(CÔNG TY CỔ PHẦN SỮA VIỆT NAM - MST: 0300588569)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Thông tin chung:</b> Vinamilk quan hệ tín dụng với 6 TCTD hàng đầu (Vietcombank, BIDV, VietinBank, HSBC, Standard Chartered, Agribank).", body_text))
    story.append(Paragraph("<b>2. Phân loại nhóm nợ:</b> <b>NHÓM 1 (NỢ ĐỦ TIÊU CHUẨN)</b> tại tất cả các TCTD. Trong lịch sử 5 năm gần nhất không phát sinh nợ cần chú ý (Nhóm 2) hoặc nợ xấu (Nhóm 3 - 5).", bold_text))
    story.append(Paragraph("<b>3. Dư nợ tại thời điểm tra cứu (31/03/2023):</b>", bold_text))
    story.append(Paragraph("- Tổng dư nợ ngắn hạn: 8.520 tỷ VND | Dư nợ trung dài hạn: 310 tỷ VND.", body_text))
    story.append(Paragraph("- Tình trạng thanh toán gốc và lãi: 100% đúng hạn, thanh khoản dồi dào.", body_text))
    story.append(Paragraph("- Điểm tín dụng CIC: <b>782 / 850 điểm - Hạng 1 (Rủi ro cực thấp)</b>.", bold_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "NGƯỜI TRA CỨU (CBTD)", "Trần Thanh Phong", SIG_TTP, "GIÁM ĐỐC TRUNG TÂM CIC", "Đoàn Thái Sơn", SIG_NHM, STAMP_CIC)
    build_doc(doc, story)
    print("✓ Đã sinh E11_01.pdf")


def gen_E2():
    doc = make_doc("E_Ho_So_Chi_Nhanh_Lap", "790000123DN0300588569_E2_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>PHÒNG QUẢN LÝ RỦI RO", "Số: 89/XHTD-2023",
               "HỆ THỐNG XẾP HẠNG TÍN DỤNG NỘI BỘ", "BAN HÀNH THEO QĐ 234/QĐ-HĐTV", "TP. Hồ Chí Minh, ngày 16 tháng 04 năm 2023")
    story.append(Paragraph("PHIẾU CHẤM ĐIỂM XẾP HẠNG TÍN DỤNG NỘI BỘ AGRIBANK<br/>KHÁCH HÀNG: CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VNM)", title_style))
    story.append(Spacer(1, 6))
    tbl_data = [
        ["Nhóm chỉ tiêu đánh giá", "Điểm chuẩn", "Điểm đạt được", "Đánh giá chi tiết"],
        ["1. Chỉ tiêu Tài chính (Thanh khoản, Đòn bẩy, Sinh lời)", "60", "58.5", "Biên lãi gộp 40.7%, ROE 24.3%, Tiền mặt >23.000 tỷ"],
        ["2. Chỉ tiêu Phi tài chính (Vị thế ngành, Ban điều hành)", "25", "25.0", "Thị phần số 1 VN, Top 6 thế giới, Quản trị minh bạch"],
        ["3. Lịch sử quan hệ tín dụng & Uy tín thanh toán", "15", "15.0", "Quan hệ tín dụng chuẩn Nhóm 1, chưa từng trễ hạn"],
        ["TỔNG ĐIỂM CHẤM ĐẠT ĐƯỢC", "100", "98.5", "XẾP HẠNG: AAA (RỦI RO CỰC THẤP)"]
    ]
    t = Table(tbl_data, colWidths=[180, 60, 75, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ae1c3f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Times'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#eafaf1")),
        ('FONTNAME', (0,4), (-1,4), 'Times-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CÁN BỘ CHẤM ĐIỂM", "Trần Thanh Phong", SIG_TTP, "TRƯỞNG PHÒNG QLRR", "Lê Văn Hùng", SIG_LVH, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh E2_01.pdf")


def gen_E3():
    doc = make_doc("E_Ho_So_Chi_Nhanh_Lap", "790000123DN0300588569_E3_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>PHÒNG KHÁCH HÀNG DOANH NGHIỆP", "Số: 112/BC-KHDN",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 17 tháng 04 năm 2023")
    story.append(Paragraph("BÁO CÁO ĐỀ XUẤT CẤP TÍN DỤNG HẠN MỨC<br/>(KHOẢN VAY VƯỢT THẨM QUYỀN - DOANH NGHIỆP VINAMILK)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Đề xuất của Phòng KHDN:</b>", bold_text))
    story.append(Paragraph("- Khách hàng: Công ty Cổ phần Sữa Việt Nam (MST: 0300588569).", body_text))
    story.append(Paragraph("- Hạn mức cấp tín dụng đề xuất: <b>3.000.000.000.000 VND</b> (Ba nghìn tỷ đồng).", body_text))
    story.append(Paragraph("- Thời hạn duy trì hạn mức: 12 tháng kể từ ngày ký HĐTD.", body_text))
    story.append(Paragraph("- Mục đích: Bổ sung vốn lưu động phục vụ thu mua sữa tươi nguyên liệu và bao bì.", body_text))
    story.append(Paragraph("- Biện pháp bảo đảm: Thế chấp Nhà máy Sữa Mega Market Bến Cát (Định giá 4.200 tỷ VND).", body_text))
    story.append(Paragraph("<b>2. Đánh giá tính khả thi và an toàn:</b> Vinamilk là khách hàng VIP truyền thống của hệ thống Agribank, dòng tiền thuần hàng năm >9.000 tỷ VND, đủ khả năng hoàn trả nợ gốc và lãi vay. Kính đề xuất Giám đốc Chi nhánh thông qua và trình cấp có thẩm quyền phê duyệt.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CÁN BỘ QUẢN LÝ KHÁCH HÀNG", "Trần Thanh Phong", SIG_TTP, "TRƯỞNG PHÒNG KHDN", "Lê Văn Hùng", SIG_LVH, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh E3_01.pdf")


def gen_E4():
    doc = make_doc("E_Ho_So_Chi_Nhanh_Lap", "790000123DN0300588569_E4_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>HỘI ĐỒNG TÍN DỤNG CƠ SỞ", "Số: 34/BB-HĐTDCS",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 17 tháng 04 năm 2023")
    story.append(Paragraph("BIÊN BẢN HỌP HỘI ĐỒNG TÍN DỤNG CƠ SỞ<br/>V/V: THÔNG QUA HỒ SƠ VAY VỐN VƯỢT THẨM QUYỀN VINAMILK", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Chủ tọa:</b> Ông Nguyễn Hoàng Minh - Giám đốc Chi nhánh, Chủ tịch HĐTDCS.", body_text))
    story.append(Paragraph("<b>Thành viên tham dự:</b> Đầy đủ 5/5 thành viên theo quy định phân quyền của Agribank.", body_text))
    story.append(Paragraph("<b>Kết quả thảo luận & biểu quyết:</b>", bold_text))
    story.append(Paragraph("- Tán thành: <b>5/5 phiếu (100%)</b> thống nhất chủ trương đề xuất cấp hạn mức 3.000 tỷ VND.", body_text))
    story.append(Paragraph("- Nhận xét: Khoản vay vượt mức phán quyết tín dụng của Giám đốc Chi nhánh TP.HCM (Hạn mức phán quyết tối đa: 500 tỷ VND).", body_text))
    story.append(Paragraph("- Quyết nghị: Giao Phòng KHDN hoàn tất hồ sơ, lập Tờ trình gửi Trung tâm Phê duyệt Miền Nam thẩm định lại và phê duyệt.", bold_text))
    story.append(Spacer(1, 25))
    add_dual_signatures(story, "THƯ KÝ HỘI ĐỒNG", "Trần Thanh Phong", SIG_TTP, "CHỦ TỊCH HỘI ĐỒNG TÍN DỤNG CƠ SỞ", "Nguyễn Hoàng Minh", SIG_NHM, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh E4_01.pdf")


def gen_E5():
    doc = make_doc("E_Ho_So_Chi_Nhanh_Lap", "790000123DN0300588569_E5_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VN<br/>AGRIBANK CHI NHÁNH TP.HCM", "Số: 45/TTr-NHNo.HCM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 18 tháng 04 năm 2023")
    story.append(Paragraph("TỜ TRÌNH PHÊ DUYỆT CẤP TÍN DỤNG VƯỢT THẨM QUYỀN<br/>KÍNH GỬI: TRUNG TÂM PHÊ DUYỆT TÍN DỤNG MIỀN NAM", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Căn cứ Quy chế cấp tín dụng của Agribank ban hành theo Quyết định số 102/QĐ-HĐTV;", body_text))
    story.append(Paragraph("Căn cứ đề nghị vay vốn của Công ty Cổ phần Sữa Việt Nam (Vinamilk);", body_text))
    story.append(Paragraph("Agribank Chi nhánh TP.HCM kính trình Trung tâm Phê duyệt Miền Nam xem xét, thẩm định lại và quyết định phê duyệt cấp tín dụng với các nội dung sau:", body_text))
    story.append(Paragraph("1. Khách hàng vay: <b>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</b>.", bold_text))
    story.append(Paragraph("2. Hạn mức cấp tín dụng: <b>3.000.000.000.000 VND</b> (Ba nghìn tỷ đồng).", bold_text))
    story.append(Paragraph("3. Tài sản bảo đảm: Nhà máy Sữa Mega Market Bến Cát (Trị giá định giá 4.200.000.000.000 VND).", body_text))
    story.append(Paragraph("4. Cam kết của Chi nhánh: Chịu trách nhiệm toàn diện về tính pháp lý của hồ sơ, kiểm soát giải ngân và thu hồi nợ đúng hạn.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "TRƯỞNG PHÒNG KHDN", "Lê Văn Hùng", SIG_LVH, "GIÁM ĐỐC CHI NHÁNH TP.HCM", "Nguyễn Hoàng Minh", SIG_NHM, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh E5_01.pdf")


# ==============================================================================
# 5. Nhóm F: Hồ sơ Trung tâm Phê duyệt lập (F.1, F.2, F.3, F.4)
# ==============================================================================
def gen_F1():
    doc = make_doc("F_Ho_So_TTPD_Lap", "790000123DN0300588569_F1_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "TRUNG TÂM PHÊ DUYỆT MIỀN NAM<br/>PHÒNG THẨM ĐỊNH TÍN DỤNG", "Mã HS: 7900.001.23.DN.0300588569",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 23 tháng 04 năm 2023")
    story.append(Paragraph("BÁO CÁO THẨM ĐỊNH LẠI ĐỘC LẬP<br/>(KHOẢN VAY VƯỢT THẨM QUYỀN - KHÁCH HÀNG VINAMILK)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Chuyên viên thẩm định lại:</b> Phạm Quốc Tuấn - Phòng Thẩm định Tín dụng TTPD.", body_text))
    story.append(Paragraph("<b>1. Đánh giá tính xác thực của hồ sơ pháp lý & kinh tế:</b> Hồ sơ pháp lý đầy đủ, Giấy ĐKKD lần 33 hợp lệ. Báo cáo tài chính kiểm toán bởi KPMG với ý kiến Chấp nhận toàn phần.", body_text))
    story.append(Paragraph("<b>2. Đánh giá khả năng tài chính & Dòng tiền:</b> Doanh thu 60.374 tỷ VND, LNST 9.019 tỷ VND. Tỷ số nợ/VCSH chỉ ở mức 0.45 lần, dòng tiền kinh doanh hàng năm thặng dư xấp xỉ 10.000 tỷ VND, hoàn toàn vượt trội so với hạn mức đề xuất 3.000 tỷ VND.", body_text))
    story.append(Paragraph("<b>3. Ý kiến đề xuất của Chuyên viên thẩm định lại:</b> <b>CHẤP THUẬN</b> cấp hạn mức tín dụng 3.000 tỷ VND kèm các điều kiện tín dụng giám sát dòng tiền qua Agribank tối thiểu 15%.", bold_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CHUYÊN VIÊN THẨM ĐỊNH LẠI", "Phạm Quốc Tuấn", SIG_PQT, "TRƯỞNG PHÒNG THẨM ĐỊNH", "Đỗ Quang Vinh", SIG_DQV, STAMP_AGRI_TTPD)
    build_doc(doc, story)
    print("✓ Đã sinh F1_01.pdf")


def gen_F2():
    doc = make_doc("F_Ho_So_TTPD_Lap", "790000123DN0300588569_F2_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "TRUNG TÂM PHÊ DUYỆT MIỀN NAM<br/>TỔ PHÁP CHẾ & TUÂN THỦ", "Số: 56/PC-TTPD",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 24 tháng 04 năm 2023")
    story.append(Paragraph("Ý KIẾN THẨM ĐỊNH PHÁP CHẾ & GIÁM SÁT TUÂN THỦ<br/>(HỒ SƠ TÍN DỤNG CÔNG TY CỔ PHẦN SỮA VIỆT NAM)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Về tư cách pháp lý và thẩm quyền ký kết:</b> Bà Mai Kiều Liên - TGĐ là đại diện pháp luật hợp pháp theo Giấy chứng nhận ĐKKD và Điều lệ công ty. Nghị quyết HĐQT số 08/NQ-HĐQT.2023 đã phân quyền đầy đủ cho TGĐ.", body_text))
    story.append(Paragraph("<b>2. Về tính pháp lý của Tài sản bảo đảm:</b> Giấy chứng nhận QSDĐ số BD-892147 do UBND tỉnh Bình Dương cấp là hợp lệ, đất thuê trả tiền một lần có quyền thế chấp theo Luật Đất đai. Chứng thư thẩm định giá Vinacontrol còn hiệu lực pháp lý.", body_text))
    story.append(Paragraph("<b>3. Kết luận Pháp chế:</b> Hồ sơ tuân thủ 100% các quy định của Luật Các TCTD và Quy chế tín dụng nội bộ Agribank. Đủ điều kiện trình Hội đồng phê duyệt.", bold_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CHUYÊN VIÊN PHÁP CHẾ", "Nguyễn Thị Mai Anh", SIG_MA, "GIÁM ĐỐC TRUNG TÂM PHÊ DUYỆT", "Đỗ Quang Vinh", SIG_DQV, STAMP_AGRI_TTPD)
    build_doc(doc, story)
    print("✓ Đã sinh F2_01.pdf")


def gen_F3():
    doc = make_doc("F_Ho_So_TTPD_Lap", "790000123DN0300588569_F3_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "TRUNG TÂM PHÊ DUYỆT MIỀN NAM<br/>HỘI ĐỒNG PHÊ DUYỆT TÍN DỤNG", "Số: 89/BB-HĐPD",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 25 tháng 04 năm 2023")
    story.append(Paragraph("BIÊN BẢN HỌP HỘI ĐỒNG PHÊ DUYỆT TÍN DỤNG TTPD<br/>V/V: PHÊ DUYỆT HỒ SƠ TÍN DỤNG VƯỢT THẨM QUYỀN VINAMILK", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Chủ trì:</b> Ông Vũ Đình Trọng - Chủ tịch Hội đồng Thẩm định & Phê duyệt Tín dụng TTPD.", body_text))
    story.append(Paragraph("<b>Thành viên HĐ:</b> Đỗ Quang Vinh (Phó Chủ tịch), Phạm Quốc Tuấn (Thư ký/Báo cáo viên), Nguyễn Thị Mai Anh (Pháp chế).", body_text))
    story.append(Paragraph("<b>Nội dung quyết nghị:</b>", bold_text))
    story.append(Paragraph("Hội đồng biểu quyết <b>5/5 phiếu (100% Tán thành)</b> phê duyệt cấp hạn mức tín dụng <b>3.000.000.000.000 VND</b> cho Vinamilk với thời hạn 12 tháng, lãi suất thỏa thuận theo biểu lãi suất Agribank từng thời kỳ.", bold_text))
    story.append(Spacer(1, 25))
    add_dual_signatures(story, "THƯ KÝ HỘI ĐỒNG PHÊ DUYỆT", "Phạm Quốc Tuấn", SIG_PQT, "CHỦ TỊCH HỘI ĐỒNG PHÊ DUYỆT", "Vũ Đình Trọng", SIG_VDT, STAMP_AGRI_TTPD)
    build_doc(doc, story)
    print("✓ Đã sinh F3_01.pdf")


def gen_F4():
    doc = make_doc("F_Ho_So_TTPD_Lap", "790000123DN0300588569_F4_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VN<br/>TRUNG TÂM PHÊ DUYỆT MIỀN NAM", "Số: 120/TB-TTPD",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 25 tháng 04 năm 2023")
    story.append(Paragraph("THÔNG BÁO PHÊ DUYỆT CẤP TÍN DỤNG VƯỢT THẨM QUYỀN<br/>KÍNH GỬI: AGRIBANK CHI NHÁNH TP. HỒ CHÍ MINH", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Trung tâm Phê duyệt Tín dụng Miền Nam thông báo quyết định của Hội đồng Phê duyệt tín dụng về việc chấp thuận cấp tín dụng vượt thẩm quyền cho Công ty Cổ phần Sữa Việt Nam như sau:", body_text))
    story.append(Paragraph("1. Khách hàng: <b>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</b>.", bold_text))
    story.append(Paragraph("2. Hạn mức cấp phê duyệt: <b>3.000.000.000.000 VND</b> (Ba nghìn tỷ đồng).", bold_text))
    story.append(Paragraph("3. Thời hạn duy trì hạn mức: 12 tháng. Mục đích: Bổ sung vốn lưu động phục vụ sản xuất.", body_text))
    story.append(Paragraph("4. Giao Giám đốc Chi nhánh TP.HCM tiến hành ký kết Hợp đồng tín dụng, hợp đồng thế chấp và quản lý giám sát giải ngân.", body_text))
    story.append(Spacer(1, 25))
    add_dual_signatures(story, "TRƯỞNG PHÒNG THẨM ĐỊNH", "Đỗ Quang Vinh", SIG_DQV, "CHỦ TỊCH HỘI ĐỒNG PHÊ DUYỆT", "Vũ Đình Trọng", SIG_VDT, STAMP_AGRI_TTPD)
    build_doc(doc, story)
    print("✓ Đã sinh F4_01.pdf")


# ==============================================================================
# 6. Nhóm G: Thông báo - Thư công tác (G.1, G.2)
# ==============================================================================
def gen_G1():
    doc = make_doc("G_Thong_Bao_Thu_Cong_Tac", "790000123DN0300588569_G1_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "TRUNG TÂM PHÊ DUYỆT MIỀN NAM<br/>TỔ THẨM ĐỊNH", "Số: 88/CV-TTPD",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 21 tháng 04 năm 2023")
    story.append(Paragraph("CÔNG VĂN YÊU CẦU BỔ SUNG GIẢI TRÌNH THUYẾT MINH CHI PHÍ<br/>KÍNH GỬI: AGRIBANK CHI NHÁNH TP. HỒ CHÍ MINH", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Trong quá trình thẩm định lại hồ sơ vay vốn của Công ty Cổ phần Sữa Việt Nam, Trung tâm Phê duyệt đề nghị Chi nhánh giải trình và làm rõ thêm các nội dung sau:", body_text))
    story.append(Paragraph("1. Cơ cấu doanh thu xuất khẩu năm 2023 và khả năng cân đối nguồn ngoại tệ.", body_text))
    story.append(Paragraph("2. Danh mục nhà cung cấp nguyên phụ liệu nhập khẩu chính và điều khoản thanh toán.", body_text))
    story.append(Paragraph("Đề nghị Chi nhánh phản hồi bằng văn bản trước ngày 22/04/2023 để hoàn tất báo cáo trình Hội đồng.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CHUYÊN VIÊN THẨM ĐỊNH", "Phạm Quốc Tuấn", SIG_PQT, "GIÁM ĐỐC TRUNG TÂM PHÊ DUYỆT", "Đỗ Quang Vinh", SIG_DQV, STAMP_AGRI_TTPD)
    build_doc(doc, story)
    print("✓ Đã sinh G1_01.pdf")


def gen_G2():
    doc = make_doc("G_Thong_Bao_Thu_Cong_Tac", "790000123DN0300588569_G2_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM", "Số: 52/CV-NHNo.HCM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 21 tháng 04 năm 2023")
    story.append(Paragraph("CÔNG VĂN GIẢI TRÌNH BỔ SUNG HỒ SƠ TÍN DỤNG VNM<br/>KÍNH GỬI: TRUNG TÂM PHÊ DUYỆT TÍN DỤNG MIỀN NAM", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Phúc đáp Công văn số 88/CV-TTPD ngày 21/04/2023, Agribank Chi nhánh TP.HCM xin báo cáo giải trình như sau:", body_text))
    story.append(Paragraph("1. Về doanh thu xuất khẩu: Chiếm ~9.5% tổng doanh thu (~5.700 tỷ VND), chủ yếu thị trường Trung Đông và Đông Nam Á. Doanh nghiệp thu ngoại tệ USD đều đặn, số dư tiền gửi ngoại tệ thanh khoản cao.", body_text))
    story.append(Paragraph("2. Về nhà cung cấp chính: Tetra Pak (Bao bì) và Fonterra (Bột sữa), hợp đồng nguyên tắc đã bổ sung tại Mục C.I.1.3.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "TRƯỞNG PHÒNG KHDN", "Lê Văn Hùng", SIG_LVH, "GIÁM ĐỐC CHI NHÁNH", "Nguyễn Hoàng Minh", SIG_NHM, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh G2_01.pdf")


# ==============================================================================
# 7. Nhóm H: Bộ hồ sơ giai đoạn giải ngân (H.1, H.2, H.3)
# ==============================================================================
def gen_H1():
    doc = make_doc("H_Ho_So_Giai_Ngan", "790000123DN0300588569_H1_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "CÔNG TY CP SỮA VIỆT NAM", "Số: 01/2023/GN-VNM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 28 tháng 04 năm 2023")
    story.append(Paragraph("GIẤY ĐỀ NGHỊ RÚT VỐN KIÊM KHẾ ƯỚC NHẬN NỢ (ĐỢT 1)<br/>CĂN CỨ HỢP ĐỒNG TÍN DỤNG HẠN MỨC SỐ 7900-LMS-2023/VNM", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Kính gửi: Ngân hàng Agribank Chi nhánh TP. Hồ Chí Minh", body_text))
    story.append(Paragraph("1. Số tiền đề nghị rút vốn: <b>500.000.000.000 VND</b> (Năm trăm tỷ đồng chẵn).", bold_text))
    story.append(Paragraph("2. Mục đích: Thanh toán tiền mua bao bì theo Hợp đồng với Tetra Pak Việt Nam.", body_text))
    story.append(Paragraph("3. Thời hạn vay: 06 tháng (Đến ngày 28/10/2023). Lãi suất: Theo thông báo lãi suất Agribank.", body_text))
    story.append(Paragraph("4. Cam kết sử dụng vốn đúng mục đích và hoàn trả nợ gốc, lãi đúng hạn.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "KẾ TOÁN TRƯỞNG", "Lê Thành Liêm", SIG_LTL, "TỔNG GIÁM ĐỐC", "Mai Kiều Liên", SIG_MKL, STAMP_VNM)
    build_doc(doc, story)
    print("✓ Đã sinh H1_01.pdf")


def gen_H2():
    doc = make_doc("H_Ho_So_Giai_Ngan", "790000123DN0300588569_H2_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>PHÒNG DỊCH VỤ KHÁCH HÀNG", "Số: 95/BC-KSGN",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 28 tháng 04 năm 2023")
    story.append(Paragraph("BÁO CÁO KIỂM TRA ĐIỀU KIỆN GIẢI NGÂN<br/>(KHÁCH HÀNG: CÔNG TY CỔ PHẦN SỮA VIỆT NAM)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Kiểm tra tính hợp lệ của Hợp đồng và TSBĐ:</b> Hợp đồng tín dụng đã ký kết đầy đủ, Hợp đồng thế chấp đã đăng ký giao dịch bảo đảm tại Văn phòng ĐKĐĐ Bình Dương hợp pháp.", body_text))
    story.append(Paragraph("<b>2. Kiểm tra chứng từ giải ngân đợt 1:</b> Hóa đơn VAT mua bao bì của Tetra Pak số 0021487 hợp lệ, Giấy đề nghị rút vốn 500 tỷ VND đúng hạn mức khả dụng.", body_text))
    story.append(Paragraph("<b>3. Kết luận:</b> Đủ điều kiện giải ngân đợt 1 số tiền 500.000.000.000 VND.", bold_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "KIỂM SOÁT VIÊN TÍN DỤNG", "Trần Thanh Phong", SIG_TTP, "TRƯỞNG PHÒNG DỊCH VỤ KHÁCH HÀNG", "Lê Văn Hùng", SIG_LVH, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh H2_01.pdf")


def gen_H3():
    doc = make_doc("H_Ho_So_Giai_Ngan", "790000123DN0300588569_H3_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM", "Số: 7900-LMS-2023/VNM",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 26 tháng 04 năm 2023")
    story.append(Paragraph("HỢP ĐỒNG TÍN DỤNG HẠN MỨC<br/>(GIỮA AGRIBANK CHI NHÁNH TP.HCM VÀ CÔNG TY CP SỮA VIỆT NAM)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Bên cho vay (Bên A):</b> Agribank Chi nhánh TP.HCM - Đại diện: Ông Nguyễn Hoàng Minh - Giám đốc.", body_text))
    story.append(Paragraph("<b>Bên vay (Bên B):</b> Công ty Cổ phần Sữa Việt Nam - Đại diện: Bà Mai Kiều Liên - Tổng Giám đốc.", body_text))
    story.append(Paragraph("<b>Điều 1: Hạn mức tín dụng: 3.000.000.000.000 VND</b> (Ba nghìn tỷ đồng chẵn).", bold_text))
    story.append(Paragraph("<b>Điều 2: Thời hạn duy trì hạn mức:</b> 12 tháng kể từ ngày ký.", body_text))
    story.append(Paragraph("<b>Điều 3: Tài sản bảo đảm:</b> Thế chấp toàn bộ Nhà máy Sữa Mega Market Bến Cát theo Hợp đồng thế chấp số 7900-TC-2023/VNM trị giá định giá 4.200 tỷ VND.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "ĐẠI DIỆN BÊN CHO VAY (AGRIBANK)", "Nguyễn Hoàng Minh", SIG_NHM, "ĐẠI DIỆN BÊN VAY (VINAMILK)", "Mai Kiều Liên", SIG_MKL, STAMP_VNM)
    build_doc(doc, story)
    print("✓ Đã sinh H3_01.pdf")


# ==============================================================================
# 8. Nhóm I: Bộ hồ sơ thu nợ & quản lý nợ (I.1, I.3)
# ==============================================================================
def gen_I1():
    doc = make_doc("I_Ho_So_Quan_Ly_No", "790000123DN0300588569_I1_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>PHÒNG KHÁCH HÀNG DOANH NGHIỆP", "Số: 21/BB-KT-2023",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Bình Dương, ngày 28 tháng 05 năm 2023")
    story.append(Paragraph("BIÊN BẢN KIỂM TRA SỬ DỤNG VỐN VAY SAU GIẢI NGÂN<br/>(KIỂM TRA LẦN ĐẦU SAU 30 NGÀY - KHÁCH HÀNG VINAMILK)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Địa điểm kiểm tra:</b> Nhà máy Sữa Việt Nam (Mega Market), TX. Bến Cát, Bình Dương.", body_text))
    story.append(Paragraph("<b>Thành phần kiểm tra:</b> Ông Trần Thanh Phong (CBTD Agribank) và Ông Lê Thành Liêm (KTT Vinamilk).", body_text))
    story.append(Paragraph("<b>Kết quả kiểm tra thực tế:</b>", bold_text))
    story.append(Paragraph("- Số tiền giải ngân 500 tỷ VND đợt 1 đã được chuyển thẳng tới tài khoản nhà cung cấp Tetra Pak theo đúng hợp đồng và hóa đơn kiểm tra.", body_text))
    story.append(Paragraph("- Hàng hóa bao bì tiệt trùng đã nhập kho đầy đủ, phục vụ dây chuyền sản xuất đang vận hành 100% công suất.", body_text))
    story.append(Paragraph("- TSBĐ (Nhà máy & Dây chuyền máy móc) được bảo quản tốt, bảo hiểm PJICO còn nguyên hiệu lực.", body_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "ĐẠI DIỆN KHÁCH HÀNG VAY", "Lê Thành Liêm", SIG_LTL, "CÁN BỘ KIỂM TRA AGRIBANK", "Trần Thanh Phong", SIG_TTP, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh I1_01.pdf")


def gen_I3():
    doc = make_doc("I_Ho_So_Quan_Ly_No", "790000123DN0300588569_I3_01.pdf")
    _, title_style, _, _, body_text, bold_text = get_styles()
    story = []
    add_header(story, "AGRIBANK CHI NHÁNH TP.HCM<br/>PHÒNG QUẢN LÝ RỦI RO", "Số: 78/BC-GS-Q3",
               "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "TP. Hồ Chí Minh, ngày 30 tháng 09 năm 2023")
    story.append(Paragraph("BÁO CÁO GIÁM SÁT ĐỊNH KỲ CHẤT LƯỢNG TÍN DỤNG QUÝ 3/2023<br/>(KHOẢN VAY VƯỢT THẨM QUYỀN - DOANH NGHIỆP VINAMILK)", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>1. Tình hình dư nợ và luân chuyển vốn:</b> Doanh số giải ngân lũy kế: 1.800 tỷ VND, doanh số thu nợ: 1.200 tỷ VND. Dư nợ hiện tại: 600 tỷ VND.", body_text))
    story.append(Paragraph("<b>2. Đánh giá chất lượng nợ:</b> Khách hàng luôn thanh toán lãi và gốc trước hạn từ 2 - 3 ngày. Dòng tiền kinh doanh luân chuyển qua tài khoản Agribank đạt 4.850 tỷ VND trong Quý 3 (vượt cam kết 15%).", body_text))
    story.append(Paragraph("<b>3. Kết luận phân loại nợ:</b> Tiếp tục duy trì <b>Nợ nhóm 1 (Đủ tiêu chuẩn)</b>. Rủi ro tín dụng ở mức tối thiểu.", bold_text))
    story.append(Spacer(1, 20))
    add_dual_signatures(story, "CÁN BỘ GIÁM SÁT RỦI RO", "Trần Thanh Phong", SIG_TTP, "TRƯỞNG PHÒNG QLRR", "Lê Văn Hùng", SIG_LVH, STAMP_AGRI_CN)
    build_doc(doc, story)
    print("✓ Đã sinh I3_01.pdf")


def main():
    print("Bắt đầu sinh các tài liệu còn lại (A12, B1_2022, B2, CI13, D3, E1-E5, F1-F4, G1-G2, H1-H3, I1, I3)...")
    gen_A12()
    gen_B1_2022()
    gen_B2()
    gen_CI13()
    gen_D3()
    gen_E11()
    gen_E2()
    gen_E3()
    gen_E4()
    gen_E5()
    gen_F1()
    gen_F2()
    gen_F3()
    gen_F4()
    gen_G1()
    gen_G2()
    gen_H1()
    gen_H2()
    gen_H3()
    gen_I1()
    gen_I3()
    print("=== ĐÃ HOÀN THÀNH SINH TẤT CẢ TÀI LIỆU CÒN LẠI THÀNH CÔNG 100% ===")

if __name__ == "__main__":
    main()
