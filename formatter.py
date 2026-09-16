import random
from datetime import datetime

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Inches, Mm, Pt, RGBColor

SPACE_INDIGO = RGBColor(0x28, 0x2C, 0x45)
GREY = RGBColor(0x80, 0x80, 0x80)
BLACK = RGBColor(0x00, 0x00, 0x00)

A4_WIDTH = Mm(210)
A4_HEIGHT = Mm(297)


def create_document():
    document = Document()

    section = document.sections[0]
    section.page_width = A4_WIDTH
    section.page_height = A4_HEIGHT

    normal_style = document.styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(14)
    # Ensure Arial is used for East Asian text runs too, not just Latin.
    rpr = normal_style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), "Arial")

    return document


def add_header(document, name_field=True, date=None, topic=None):
    title = document.add_paragraph()
    title_run = title.add_run("Rant Circle")
    title_run.font.size = Pt(34)
    title_run.font.bold = True
    title_run.font.color.rgb = SPACE_INDIGO

    if name_field:
        name_paragraph = document.add_paragraph()
        name_run = name_paragraph.add_run("Name: ___________________")
        name_run.font.color.rgb = BLACK

    date_paragraph = document.add_paragraph()
    if date:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %-d, %Y")
    else:
        formatted_date = datetime.today().strftime("%B %-d, %Y")
    date_run = date_paragraph.add_run(f"Date: {formatted_date}")
    date_run.font.color.rgb = BLACK

    topic_paragraph = document.add_paragraph()
    topic_run = topic_paragraph.add_run(f"Topic: {topic if topic else 'General'}")
    topic_run.font.color.rgb = BLACK


def add_page1_content(document, topic_slug=None):
    with open("config/phrases.yaml", "r") as f:
        phrases = yaml.safe_load(f)
    checkin_question = random.choice(phrases["checkin_questions"])

    checkin_paragraph = document.add_paragraph()
    label_run = checkin_paragraph.add_run("Warm-Up: ")
    label_run.font.bold = True
    label_run.font.color.rgb = SPACE_INDIGO
    question_run = checkin_paragraph.add_run(checkin_question)
    question_run.font.color.rgb = BLACK

    for placeholder in (
        "[Topic-primer question 1 — generated in Phase 3]",
        "[Topic-primer question 2 — generated in Phase 3]",
    ):
        placeholder_paragraph = document.add_paragraph()
        placeholder_run = placeholder_paragraph.add_run(placeholder)
        placeholder_run.font.color.rgb = BLACK
        placeholder_run.font.italic = True


def add_footer(document):
    footer = document.sections[0].footer
    footer_paragraph = footer.paragraphs[0]
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_paragraph.add_run("www.primo-english.xyz")
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = GREY

    page_number_paragraph = footer.add_paragraph()
    page_number_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    run = page_number_paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr_text)
    run._r.append(fld_end)


def _set_paragraph_bottom_border(paragraph, color_hex="282C45", size="6"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_borders = OxmlElement("w:pBdr")
    bottom_border = OxmlElement("w:bottom")
    bottom_border.set(qn("w:val"), "single")
    bottom_border.set(qn("w:sz"), size)
    bottom_border.set(qn("w:space"), "1")
    bottom_border.set(qn("w:color"), color_hex)
    p_borders.append(bottom_border)
    p_pr.append(p_borders)


def add_section_divider(document, text=None):
    if text:
        label_paragraph = document.add_paragraph()
        label_run = label_paragraph.add_run(text)
        label_run.font.size = Pt(9)
        label_run.font.bold = True
        label_run.font.color.rgb = SPACE_INDIGO

    divider_paragraph = document.add_paragraph()
    _set_paragraph_bottom_border(divider_paragraph)


def _add_open_prompt(document, prompt_text, blank_lines):
    prompt_paragraph = document.add_paragraph()
    prompt_run = prompt_paragraph.add_run(prompt_text)
    prompt_run.font.bold = True
    prompt_run.font.color.rgb = SPACE_INDIGO

    for _ in range(blank_lines):
        document.add_paragraph()


def add_speaker_prep_sheet(document):
    document.add_page_break()

    title_paragraph = document.add_paragraph()
    title_run = title_paragraph.add_run("Time to Start Cooking...a Rant!")
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = SPACE_INDIGO

    _add_open_prompt(document, "What's on your mind?", blank_lines=3)
    _add_open_prompt(document, "The main feeling behind it", blank_lines=2)
    _add_open_prompt(
        document, "Have you already said or done anything about it?", blank_lines=2
    )

    feedback_label = document.add_paragraph()
    feedback_label_run = feedback_label.add_run("What kind of feedback would you like?")
    feedback_label_run.font.bold = True
    feedback_label_run.font.color.rgb = SPACE_INDIGO

    feedback_options = [
        ("Practical advice", "A reality check"),
        ("Nothing. I just want to vent.", "Any of the above"),
    ]
    feedback_table = document.add_table(rows=2, cols=2)
    for row_idx, (left_text, right_text) in enumerate(feedback_options):
        for col_idx, option_text in enumerate((left_text, right_text)):
            cell_paragraph = feedback_table.cell(row_idx, col_idx).paragraphs[0]
            cell_run = cell_paragraph.add_run(f"□ {option_text}")
            cell_run.font.color.rgb = BLACK

    words_label = document.add_paragraph()
    words_label_run = words_label.add_run("Maybe useful words")
    words_label_run.font.bold = True
    words_label_run.font.color.rgb = SPACE_INDIGO

    words_table = document.add_table(rows=1, cols=5)
    words_table.autofit = False
    column_widths = [Inches(1.7), Inches(0.25), Inches(1.7), Inches(0.25), Inches(1.7)]
    for col_idx, width in enumerate(column_widths):
        words_table.columns[col_idx].width = width
        words_table.cell(0, col_idx).width = width

    for col_idx in (0, 2, 4):
        blank_paragraph = words_table.cell(0, col_idx).paragraphs[0]
        _set_paragraph_bottom_border(blank_paragraph, color_hex="000000")


if __name__ == "__main__":
    document = create_document()
    add_footer(document)
    add_header(document, name_field=True, date="2026-09-16", topic="Work Hours")
    add_page1_content(document, topic_slug="workhours")
    document.add_paragraph("This is a test of the document skeleton.")
    add_section_divider(document, text="Test Divider")
    add_speaker_prep_sheet(document)
    document.save("output/skeleton_test.docx")
    print("Saved output/skeleton_test.docx")
