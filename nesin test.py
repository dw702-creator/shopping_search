import streamlit as st
from docx import Document
from docx.shared import Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import tempfile


def set_cell_border(cell, top=True, bottom=True, left=True, right=True):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')

    def add_border(name):
        border = OxmlElement(f'w:{name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '6')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'auto')
        borders.append(border)

    if top:
        add_border('top')
    if bottom:
        add_border('bottom')
    if left:
        add_border('left')
    if right:
        add_border('right')

    tcPr.append(borders)


def create_exam_doc(text):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

    sentences = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        sentences.extend([s.strip() for s in line.split(".") if s.strip()])

    for s in sentences:
        table = doc.add_table(rows=1, cols=2)
        table.autofit = False

        left = table.cell(0, 0)
        right = table.cell(0, 1)

        left.width = Cm(8)
        right.width = Cm(8)

        set_cell_border(left, top=True, bottom=True, left=True, right=True)
        set_cell_border(right, top=True, bottom=True, left=False, right=True)

        left.paragraphs[0].text = s + "."
        for _ in range(6):
            right.add_paragraph("")

        doc.add_paragraph("")

    return doc


# ---------------- Streamlit UI ---------------- #

st.set_page_config(page_title="Blank Test Generator", layout="centered")

st.title("Blank Test Generator")
st.write("텍스트를 입력하면 **문제 + 메모형 시험지 Word 파일**을 생성합니다.")

input_text = st.text_area(
    "분석할 영어 지문을 입력하세요",
    height=300,
    placeholder="여기에 시험지 텍스트를 붙여 넣으세요."
)

if st.button("시험지 생성"):
    if not input_text.strip():
        st.warning("텍스트를 입력해주세요.")
    else:
        doc = create_exam_doc(input_text)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(tmp.name)

        with open(tmp.name, "rb") as f:
            st.download_button(
                label="Word 파일 다운로드",
                data=f,
                file_name="시험지_분석용.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
