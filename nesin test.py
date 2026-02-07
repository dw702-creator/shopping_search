from docx import Document
from docx.shared import Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


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


def create_exam_doc(text, filename="시험지.docx"):
    doc = Document()

    # 여백 설정
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines:
        # 문제 하나당 테이블 하나
        table = doc.add_table(rows=1, cols=2)
        table.autofit = False

        left_cell = table.cell(0, 0)
        right_cell = table.cell(0, 1)

        left_cell.width = Cm(8)
        right_cell.width = Cm(8)

        # 문제 ↔ 메모 구분선 + 문제 간 구분선
        set_cell_border(left_cell, top=True, bottom=True, left=True, right=True)
        set_cell_border(right_cell, top=True, bottom=True, left=False, right=True)

        # 왼쪽: 문제 텍스트 (번호 없음)
        p = left_cell.paragraphs[0]
        p.text = line
        p.paragraph_format.space_after = Cm(0.4)

        # 오른쪽: 메모 공간
        for _ in range(6):
            right_cell.add_paragraph("")

        doc.add_paragraph("")  # 문제 사이 여백

    doc.save(filename)
    return filename


if __name__ == "__main__":
    sample_text = """Artificial intelligence is changing education.
Students use AI tools for writing assignments.
Teachers need new ways to assess learning outcomes."""

    create_exam_doc(sample_text, "메모형_시험지.docx")
