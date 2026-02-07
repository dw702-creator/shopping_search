import streamlit as st
from docx import Document
from docx.shared import Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import tempfile


def set_vertical_border(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')

    border = OxmlElement('w:right')
    border.set(qn('w:val'), 'single')
    border.set(qn('w:sz'), '8')
    border.set(qn('w:space'), '0')
    border.set(qn('w:color'), 'auto')

    borders.append(border)
    tcPr.append(borders)


def create_exam_doc(text):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = False

    left_cell = table.cell(0, 0)
    right_cell = table.cell(0, 1)

    left_cell.width = Cm(8)
    right_cell.width = Cm(8)

    # 시험지 ↔ 메모칸 사이 세로 구분선
    set_vertical_border(left_cell)

    # 왼쪽: 입력 텍스트 그대로
    left_cell.paragraphs[0].text = text

    # 오른쪽: 메모용 빈 줄
    for _ in range(25):
        right_cell.add_paragraph("")

    return doc


# ---------------- Streamlit UI ---------------- #

st.set_page_config(page_title="Blank Test Generator", layout="centered")

st.title("Blank Test Generator")
st.write("입력한 텍스트를 **왼쪽 시험지 / 오른쪽 메모용** Word 파일로 변환합니다.")

input_text = st.text_area(
    "분석할 시험지 텍스트를 그대로 붙여 넣으세요",
    height=350,
    placeholder="여기에 시험지 원문을 그대로 붙여 넣으세요."
)

if st.button("Word 파일 생성"):
    if not input_text.strip():
        st.warning("텍스트를 입력해주세요.")
    else:
        doc = create_exam_doc(input_text)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(tmp.name)

        with open(tmp.name, "rb") as f:
            st.download_button(
                label="다운로드",
                data=f,
                file_name="시험지_분석용.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
