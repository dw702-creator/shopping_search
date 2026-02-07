import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
import os
import re

# ---------------- PDF 텍스트 추출 ----------------
def extract_text_pdfplumber(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text.strip()

# ---------------- OCR 처리 ----------------
def extract_text_ocr(file_bytes):
    images = convert_from_bytes(file_bytes)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="eng") + "\n"
    return text.strip()

# ---------------- 텍스트 정리 ----------------
def clean_text(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

# ---------------- 시험지 PDF 생성 ----------------
def create_exam_pdf(text, original_filename):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = {
        "title": ParagraphStyle(
            "title",
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20,
            leading=22
        ),
        "info": ParagraphStyle(
            "info",
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=20
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=11,
            leading=16,
            spaceAfter=12
        )
    }

    story = []

    # 제목
    story.append(Paragraph("연세영어학원", styles["title"]))
    story.append(Paragraph(
        "반: ________ &nbsp;&nbsp;&nbsp; 이름: ________ &nbsp;&nbsp;&nbsp; 점수: ________ &nbsp;&nbsp;&nbsp; 선생님 확인: ________",
        styles["info"]
    ))
    story.append(Spacer(1, 12))

    for para in text.split("\n\n"):
        story.append(Paragraph(para, styles["body"]))

    doc.build(story)
    buffer.seek(0)

    base = os.path.splitext(original_filename)[0]
    output_name = f"{base}_OCR시험지.pdf"

    return buffer, output_name

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Blank Test Generator (OCR PDF)", layout="wide")
st.title("📄 Blank Test Generator (OCR PDF)")
st.markdown("텍스트 PDF와 **스캔 PDF(OCR)** 모두 지원하여 깔끔한 시험지 PDF로 재생성합니다.")

uploaded_pdf = st.file_uploader("PDF 파일 업로드", type=["pdf"])

if uploaded_pdf:
    if st.button("시험지 PDF 생성"):
        try:
            file_bytes = uploaded_pdf.read()

            # 1차: 텍스트 PDF 시도
            text = extract_text_pdfplumber(BytesIO(file_bytes))

            # 실패 시 OCR
            if not text:
                st.info("텍스트 PDF가 아니어서 OCR을 실행합니다...")
                text = extract_text_ocr(file_bytes)

            if not text:
                st.error("PDF에서 텍스트를 인식하지 못했습니다.")
            else:
                clean = clean_text(text)
                pdf_buffer, filename = create_exam_pdf(clean, uploaded_pdf.name)

                st.success("시험지 PDF가 생성되었습니다!")
                st.download_button(
                    label="⬇️ 시험지 PDF 다운로드",
                    data=pdf_buffer,
                    file_name=filename,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("PDF 처리 중 오류가 발생했습니다.")
            st.exception(e)
else:
    st.info("PDF 파일을 업로드하세요.")
