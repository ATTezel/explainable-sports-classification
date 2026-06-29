#!/usr/bin/env python3
"""Builds the Phase III submission cover document (submission_links.docx) and the
literal text-file the professor asked for (submission_overleaf_link.txt).

Modeled on a reference submission: a links table (Item | Description | Status),
an Additional-Files list, and a Key-Results summary.

Run:  ~/homework/Assignment3-Classifiers/.venv/bin/python build_docx.py
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- canonical facts (edit the [PASTE ...] links after you create them) ----
STUDENT      = "Arda Tekin Tezel"
EMAIL        = "arda.t.tezel@gmail.com"          # or your @ue-germany.de address
INSTITUTION  = "University of Europe for Applied Sciences, Potsdam"
TOPIC        = "Explainable Sports Category Classification Using CNN Transfer Learning"

GITHUB   = "https://github.com/ATTezel/explainable-sports-classification"   # already live
DATASET  = "https://www.kaggle.com/datasets/gpiosenka/sports-classification"
NOTEBOOK = "https://www.kaggle.com/code/ardatezel/explainable-sports-classification"
OVERLEAF = "[PASTE your EDITABLE Overleaf link here — Share > Anyone can edit]"
WEBAPP   = "[PASTE your Hugging Face Spaces link after you deploy app/]"
VIDEO    = "[PASTE your YouTube/loom presentation link after you record it]"
PROMPTLOG = "[OPTIONAL: PASTE your claude.ai shared-conversation link]"

NAVY = RGBColor(0x21, 0x39, 0x52)
TEAL = RGBColor(0x2C, 0x7A, 0x7B)
GREY = RGBColor(0x55, 0x63, 0x74)
HEADER_BG = "21394F"
ROW_ALT   = "EEF4FB"


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def set_run(run, size, color=None, bold=False, italic=False, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font
    if color is not None:
        run.font.color.rgb = color


def cell_text(cell, text, size=10, color=None, bold=False, italic=False, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_run(r, size, color, bold, italic)
    return p


doc = Document()
# base style
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
for sec in doc.sections:
    sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.9); sec.right_margin = Inches(0.9)

# ---- header block ----
p = doc.add_paragraph(); r = p.add_run("MACHINE LEARNING & SMART SYSTEMS")
set_run(r, 11, TEAL, bold=True)
p = doc.add_paragraph(); r = p.add_run("Phase III — Final Report and Presentation")
set_run(r, 19, NAVY, bold=True)
p.space_after = Pt(2)
p = doc.add_paragraph(); r = p.add_run(TOPIC); set_run(r, 12.5, NAVY, italic=True, bold=True)
# horizontal rule
pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "6"); bottom.set(qn("w:space"), "4")
bottom.set(qn("w:color"), "C7D2E0"); pbdr.append(bottom); pPr.append(pbdr)

p = doc.add_paragraph()
r = p.add_run("Student:  "); set_run(r, 11, bold=True)
r = p.add_run(STUDENT + "        "); set_run(r, 11)
r = p.add_run("Email:  "); set_run(r, 11, bold=True)
r = p.add_run(EMAIL); set_run(r, 11)
p = doc.add_paragraph()
r = p.add_run("Institution:  "); set_run(r, 11, bold=True)
r = p.add_run(INSTITUTION); set_run(r, 11)

# ---- submission links ----
p = doc.add_paragraph(); r = p.add_run("Submission Links"); set_run(r, 14, NAVY, bold=True)
p = doc.add_paragraph(
    "Dear Professor, please find all submission links below. The system classifies the sport "
    "depicted in an image across 100 categories and explains each decision with Grad-CAM and SHAP. "
    "Three CNN models were trained and compared, and the best-balanced model was deployed as a live web demo.")
for r_ in p.runs:
    set_run(r_, 10.5)

items = [
    ("1. Dataset",
     "100 Sports Image Classification dataset (Kaggle, gpiosenka), used to train and evaluate the three CNN models.",
     DATASET, "Ready"),
    ("2. Kaggle notebook",
     "End-to-end notebook: 3 CNN models, training, evaluation, Grad-CAM and SHAP, exporting all figures and metrics.",
     NOTEBOOK, "Ready"),
    ("3. GitHub repository",
     "Public repository with the notebook, the front-end app code, the LaTeX report, figures, and README.",
     GITHUB, "Ready"),
    ("4. Overleaf report (editable)",
     "Editable project report on Overleaf in the provided template, shared with edit access. This is the graded artifact.",
     OVERLEAF, "Create & paste"),
    ("5. Frontend website",
     "Live, interactive web demo on Hugging Face Spaces (Gradio): upload an image and get the top-5 sports, confidence, and a Grad-CAM heatmap.",
     WEBAPP, "Deploy & paste"),
    ("6. Presentation video",
     "Recorded walkthrough (max 10 min): ~2 min live demo of the web interface + ~8 min slides.",
     VIDEO, "Record & paste"),
    ("7. Prompt log (optional)",
     "Shared conversation link documenting the prompts and process in one place.",
     PROMPTLOG, "Optional"),
]
tbl = doc.add_table(rows=1 + len(items), cols=3)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.style = "Table Grid"
widths = [Inches(1.7), Inches(4.6), Inches(1.3)]
hdr = tbl.rows[0].cells
for j, h in enumerate(["Item", "Description", "Status"]):
    shade(hdr[j], HEADER_BG)
    cell_text(hdr[j], h, size=10.5, color=RGBColor(0xFF, 0xFF, 0xFF), bold=True)
for i, (name, desc, link, status) in enumerate(items, start=1):
    cells = tbl.rows[i].cells
    if i % 2 == 0:
        for c in cells:
            shade(c, ROW_ALT)
    cell_text(cells[0], name, size=10.5, color=NAVY, bold=True)
    # description + link
    cells[1].text = ""
    pp = cells[1].paragraphs[0]; rr = pp.add_run(desc); set_run(rr, 10)
    pp2 = cells[1].add_paragraph(); rr2 = pp2.add_run(link)
    set_run(rr2, 10, RGBColor(0x1A, 0x57, 0xB6))
    cell_text(cells[2], status, size=10, color=(RGBColor(0x1E,0x7A,0x34) if status=="Ready" else GREY),
              bold=(status == "Ready"))
for row in tbl.rows:
    for j, w in enumerate(widths):
        row.cells[j].width = w

# ---- additional files ----
doc.add_paragraph()
p = doc.add_paragraph(); r = p.add_run("Additional Files (submitted alongside this document)")
set_run(r, 12.5, NAVY, bold=True)
for txt, tail in [
    ("Report PDF", " — exported from the Overleaf link above (initial reference copy)."),
    ("Presentation file (PowerPoint)", " — the slide deck used in the presentation video."),
]:
    pp = doc.add_paragraph(style="List Bullet")
    r = pp.add_run(txt); set_run(r, 10.5, bold=True)
    r = pp.add_run(tail); set_run(r, 10.5)

# ---- key results ----
p = doc.add_paragraph(); r = p.add_run("Key Results (Test Set)"); set_run(r, 12.5, NAVY, bold=True)
p = doc.add_paragraph(); r = p.add_run("All figures below are from the executed Kaggle run (results.json); the report and the code agree exactly.")
set_run(r, 9.5, RGBColor(0x1E, 0x7A, 0x34), italic=True)
for lead, tail in [
    ("Custom CNN — ", "47.2% accuracy, 0.429 macro-F1 (from-scratch baseline; 0.48M params, 1.9 MB, 0.6 ms/image)."),
    ("EfficientNetV2-B0 — ", "96.2% accuracy, 0.960 macro-F1; near-identical accuracy at ~1/5 the size and ~1/12 the latency (6.0M params, 24 MB, 9.6 ms) — best efficiency trade-off."),
    ("ConvNeXt-Tiny — ", "96.4% accuracy, 0.963 macro-F1; the most accurate model, deployed as the best model (27.9M params, 112 MB, 113 ms)."),
]:
    pp = doc.add_paragraph(style="List Bullet")
    r = pp.add_run(lead); set_run(r, 10.5, bold=True)
    r = pp.add_run(tail); set_run(r, 10.5)
p = doc.add_paragraph()
r = p.add_run("Takeaway: ")
set_run(r, 10.5, bold=True)
r = p.add_run("transfer learning clearly beats the from-scratch baseline, and Grad-CAM + SHAP confirm the "
              "model attends to athletes and equipment rather than the background — accuracy with accountability.")
set_run(r, 10.5, italic=True)

doc.add_paragraph()
p = doc.add_paragraph(); r = p.add_run("Thank you for your time. I am happy to answer any questions.")
set_run(r, 10.5)
p = doc.add_paragraph(); r = p.add_run("Best regards,"); set_run(r, 10.5)
p = doc.add_paragraph(); r = p.add_run(STUDENT); set_run(r, 10.5, bold=True)

out = os.path.join(HERE, "submission_links.docx")
doc.save(out)
print("wrote", out)

# ---- literal required text file ----
txt = os.path.join(HERE, "submission_overleaf_link.txt")
with open(txt, "w") as f:
    f.write(
        "PHASE III SUBMISSION — Editable Overleaf Link\n"
        "Machine Learning & Smart Systems · Topic 12.4\n"
        f"Explainable Sports Category Classification\n"
        f"Student: {STUDENT}\n\n"
        "Editable Overleaf report link (Share > Anyone with this link can EDIT):\n"
        f"{OVERLEAF}\n\n"
        "Supporting links:\n"
        f"  GitHub repository : {GITHUB}\n"
        f"  Dataset           : {DATASET}\n"
        f"  Kaggle notebook   : {NOTEBOOK}\n"
        f"  Live web demo     : {WEBAPP}\n"
        f"  Presentation video: {VIDEO}\n")
print("wrote", txt)
