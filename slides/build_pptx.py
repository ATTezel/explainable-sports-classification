#!/usr/bin/env python3
"""Builds sports_cnn_presentation.pptx — a clean 12-slide deck for the
Explainable Sports Category Classification project, styled after a polished
reference submission (navy titles, light-blue cards, callout boxes, results table).

Run:  ~/homework/Assignment3-Classifiers/.venv/bin/python build_pptx.py

Figures: if a figure file exists under ../report/figures/ it is embedded;
otherwise a labelled placeholder box is drawn so you can drop the real figure
(from the Kaggle run's results.zip) into the same box later.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "report", "figures")

# ---- palette ---------------------------------------------------------------
NAVY      = RGBColor(0x21, 0x39, 0x52)   # titles
INK       = RGBColor(0x1F, 0x2A, 0x37)   # body text
TEAL      = RGBColor(0x2C, 0x7A, 0x7B)   # section label
SUBTITLE  = RGBColor(0x33, 0x47, 0x60)   # subtitle
CARD_BG   = RGBColor(0xDD, 0xEA, 0xF7)   # light blue card
CARD_BG2  = RGBColor(0xEE, 0xF4, 0xFB)   # lighter card
DARKCARD  = RGBColor(0x1B, 0x2A, 0x4A)   # dark highlight card
GREEN_BG  = RGBColor(0xD9, 0xF0, 0xDE)
GREEN_TX  = RGBColor(0x1E, 0x7A, 0x34)
RED_BG    = RGBColor(0xF9, 0xDA, 0xDD)
RED_TX    = RGBColor(0xB0, 0x2A, 0x37)
GREY_TX   = RGBColor(0x55, 0x63, 0x74)
PLACE_BG  = RGBColor(0xF1, 0xF4, 0xF8)
PLACE_LN  = RGBColor(0xB6, 0xC4, 0xD6)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT    = RGBColor(0x2F, 0x6F, 0xD6)

FONT = "Calibri"
FONT_L = "Calibri Light"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def slide():
    s = prs.slides.add_slide(BLANK)
    # white background
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    return s


def _set(run, size, color, bold=False, italic=False, font=FONT):
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font


def textbox(s, x, y, w, h, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, wrap=True):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    return tf


def para(tf, text, size, color, bold=False, italic=False, font=FONT,
         align=PP_ALIGN.LEFT, space_after=6, space_before=0, bullet=None, level=0,
         first=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.level = level
    if space_after is not None:
        p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    if bullet:
        run = p.add_run(); _set(run, size, color, bold=True, font=font); run.text = bullet + "  "
    run = p.add_run()
    _set(run, size, color, bold=bold, italic=italic, font=font)
    run.text = text
    return p


def rounded(s, x, y, w, h, fill, line=None, line_w=1.25, radius=0.08):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.adjustments[0] = radius
    except Exception:
        pass
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def card(s, x, y, w, h, heading, body, fill=CARD_BG, head_color=NAVY,
         body_color=INK, head_size=18, body_size=13, number=None):
    rounded(s, x, y, w, h, fill)
    pad = 0.22
    tf = textbox(s, x + pad, y + pad, w - 2 * pad, h - 2 * pad)
    if number is not None:
        para(tf, number, 26, ACCENT, bold=True, first=True, space_after=2)
        para(tf, heading, head_size, head_color, bold=True, space_after=6)
    else:
        para(tf, heading, head_size, head_color, bold=True, first=True, space_after=6)
    for b in (body if isinstance(body, list) else [body]):
        para(tf, b, body_size, body_color, space_after=4)
    return tf


def callout(s, x, y, w, h, text, fill=CARD_BG, text_color=NAVY, icon=None,
            title=None, size=13):
    rounded(s, x, y, w, h, fill)
    pad = 0.22
    tf = textbox(s, x + pad, y + pad, w - 2 * pad, h - 2 * pad,
                 anchor=MSO_ANCHOR.MIDDLE)
    if title:
        head = (icon + "  " if icon else "") + title
        para(tf, head, 15, text_color, bold=True, first=True, space_after=4)
        para(tf, text, size, text_color, space_after=0)
    else:
        para(tf, (icon + "  " if icon else "") + text, size, text_color,
             first=True, space_after=0)
    return tf


def header(s, label, title, subtitle, title_size=34):
    textbox(s, 0.7, 0.45, 12, 0.5)
    tf = textbox(s, 0.7, 0.42, 12, 0.45)
    para(tf, label.upper(), 12.5, TEAL, bold=True, first=True, space_after=2)
    tf2 = textbox(s, 0.7, 0.78, 12, 1.0)
    para(tf2, title, title_size, NAVY, bold=True, first=True, space_after=2, font=FONT_L)
    tf3 = textbox(s, 0.7, 0.78 + title_size / 58.0, 12, 0.5)
    para(tf3, subtitle, 17, SUBTITLE, bold=True, first=True, space_after=0)
    # thin rule
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.74),
                            Inches(11.93), Pt(2))
    ln.fill.solid(); ln.fill.fore_color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    ln.line.fill.background(); ln.shadow.inherit = False


def figure(s, fname, x, y, w, h, caption=None):
    path = os.path.join(FIG, fname)
    if os.path.exists(path):
        iw = ih = None
        if HAVE_PIL:
            try:
                with Image.open(path) as im:
                    iw, ih = im.size
            except Exception:
                iw = ih = None
        if iw and ih:
            scale = min(w / (iw / 96.0), h / (ih / 96.0))
            pw = (iw / 96.0) * scale
            ph = (ih / 96.0) * scale
            px = x + (w - pw) / 2
            py = y + (h - ph) / 2
            s.shapes.add_picture(path, Inches(px), Inches(py),
                                 Inches(pw), Inches(ph))
        else:
            s.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w))
    else:
        shp = rounded(s, x, y, w, h, PLACE_BG, line=PLACE_LN, line_w=1.25, radius=0.03)
        tf = textbox(s, x, y, w, h, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        para(tf, "🖼  " + fname, 14, GREY_TX, bold=True, first=True,
             align=PP_ALIGN.CENTER, space_after=4)
        para(tf, "paste from results.zip (Kaggle run)", 11, GREY_TX,
             italic=True, align=PP_ALIGN.CENTER, space_after=0)
    if caption:
        tf = textbox(s, x, y + h + 0.02, w, 0.3, align=PP_ALIGN.CENTER)
        para(tf, caption, 10.5, GREY_TX, italic=True, first=True,
             align=PP_ALIGN.CENTER, space_after=0)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


REPLACE = "⚠ PLACEHOLDER NUMBERS — replace with your real Kaggle results before recording."

# ======================================================================
# Slide 1 — Title
# ======================================================================
s = slide()
# left accent bar
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), SH)
bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
bar.shadow.inherit = False

tf = textbox(s, 1.0, 1.5, 11.3, 0.5)
para(tf, "MACHINE LEARNING & SMART SYSTEMS  ·  TOPIC 12.4", 14, TEAL, bold=True, first=True)
tf = textbox(s, 0.95, 2.05, 11.5, 2.2)
para(tf, "Explainable Sports Category", 46, NAVY, bold=True, first=True,
     space_after=0, font=FONT_L)
para(tf, "Classification", 46, NAVY, bold=True, space_after=8, font=FONT_L)
tf = textbox(s, 1.0, 4.05, 11.3, 0.8)
para(tf, "CNN transfer learning with Grad-CAM & SHAP — 100-class image recognition",
     20, SUBTITLE, bold=True, first=True)
# author block
tf = textbox(s, 1.0, 5.3, 6.2, 1.6)
para(tf, "Arda Tekin Tezel", 18, INK, bold=True, first=True, space_after=2)
para(tf, "Machine Learning & Smart Systems", 14, GREY_TX, space_after=0)
para(tf, "University of Europe for Applied Sciences, Potsdam", 14, GREY_TX, space_after=0)
tf = textbox(s, 7.3, 5.3, 5.0, 1.6)
para(tf, "Final Project — Phase III", 14, GREY_TX, first=True, space_after=2)
para(tf, "100-class image classification", 14, GREY_TX, space_after=2)
para(tf, "Custom CNN  ·  EfficientNetV2-B0  ·  ConvNeXt-Tiny", 14, NAVY, bold=True, space_after=0)
notes(s, "Title slide. Introduce yourself, the topic (12.4), and the three models. ~20s.")

# ======================================================================
# Slide 2 — Problem & Motivation
# ======================================================================
s = slide()
header(s, "Problem & Motivation", "Why classify sports images — and why explain it?",
       "Accuracy alone is not enough for a trustworthy system")
cw, cy, ch = 3.82, 2.05, 2.55
gap = 0.22
xs = 0.7
cards = [
    ("Scale", ["Sports media platforms and archives hold millions of images that must be tagged by sport for search, indexing, and broadcast analytics."]),
    ("Manual tagging fails", ["Hand-labelling across 100+ categories is slow, costly, and inconsistent — it simply does not scale."]),
    ("Explainability is essential", ["A model can be right for the wrong reasons. We must verify it looks at the athlete and equipment, not the background."]),
]
for i, (h_, b_) in enumerate(cards):
    card(s, xs + i * (cw + gap), cy, cw, ch, h_, b_)
callout(s, 0.7, 4.95, 11.93, 1.35,
        "An accurate AND interpretable 100-class sports classifier, deployed as a live web demo whose every decision can be inspected with Grad-CAM and SHAP.",
        fill=CARD_BG2, text_color=NAVY, icon="🎯", title="Goal")
notes(s, "Motivate the task and stress why explainability matters for trust. ~40s.")

# ======================================================================
# Slide 3 — Dataset & Preprocessing
# ======================================================================
s = slide()
header(s, "Data & Preprocessing", "100 Sports Image Classification (Kaggle, gpiosenka)",
       "From raw images to a model-ready pipeline")
cw, cy, ch = 3.82, 2.05, 2.05
cards = [
    ("100 classes", ["~14,500 RGB images spanning 100 sports, from air hockey to wingsuit flying."]),
    ("Fixed splits", ["13,493 train / 500 validation / 500 test, all standardised to 224 x 224 x 3."]),
    ("Augmentation", ["Horizontal flip, small rotation, zoom and contrast — applied to the training set only."]),
]
for i, (h_, b_) in enumerate(cards):
    card(s, 0.7 + i * (cw + 0.22), cy, cw, ch, h_, b_)
# two small figure placeholders
figure(s, "sample_grid.png", 0.7, 4.35, 5.85, 2.6, "Sample images (one per class)")
figure(s, "class_distribution.png", 6.78, 4.35, 5.85, 2.6, "Class distribution — near-balanced")
notes(s, "Describe the dataset and preprocessing. Point to the sample grid and the near-balanced distribution. ~40s.")

# ======================================================================
# Slide 4 — Research Questions
# ======================================================================
s = slide()
header(s, "Research Questions", "Five questions guide the study",
       "From model choice to a deployable, explainable prototype")
rqs = [
    ("RQ1", "Which architecture classifies 100 sports most accurately?"),
    ("RQ2", "Does ImageNet transfer learning beat a custom CNN trained from scratch?"),
    ("RQ3", "Do Grad-CAM and SHAP show the model attends to athletes and equipment, not the background?"),
    ("RQ4", "Which model gives the best accuracy / speed / size trade-off?"),
    ("RQ5", "Can the best model be deployed as a working, explainable web demo?"),
]
y = 2.1
for tag, q in rqs:
    rounded(s, 0.7, y, 1.15, 0.78, NAVY)
    tf = textbox(s, 0.7, y, 1.15, 0.78, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    para(tf, tag, 17, WHITE, bold=True, first=True, align=PP_ALIGN.CENTER, space_after=0)
    tf = textbox(s, 2.05, y, 10.5, 0.78, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, q, 16, INK, first=True, space_after=0)
    y += 0.95
notes(s, "Read the five research questions; they structure the whole talk. ~35s.")

# ======================================================================
# Slide 5 — Methodology pipeline
# ======================================================================
s = slide()
header(s, "Methodology", "From raw images to an explainable web app",
       "A single, reproducible pipeline (seed 42)")
figure(s, "workflow.png", 0.7, 2.0, 11.93, 4.55)
notes(s, "Walk left to right through the pipeline: data -> preprocess/augment -> 3 models -> "
         "evaluate -> Grad-CAM/SHAP -> deploy. Everything is seeded for reproducibility. ~45s.")

# ======================================================================
# Slide 6 — Three models compared
# ======================================================================
s = slide()
header(s, "Models", "Three architectures, one classification task",
       "A lightweight baseline versus two pretrained backbones")
cw, cy, ch = 3.82, 2.1, 3.05
models = [
    ("1", "Custom CNN", ["From scratch; 4 convolutional blocks (32 -> 256).",
                          "BatchNorm + MaxPool; global average pooling.",
                          "Lightweight baseline."]),
    ("2", "EfficientNetV2-B0", ["ImageNet pretrained; transfer learning.",
                                 "Two-phase fine-tuning; ~6-7M parameters.",
                                 "Efficiency-focused."]),
    ("3", "ConvNeXt-Tiny", ["ImageNet pretrained; modern ConvNet.",
                             "Two-phase fine-tuning; ~28M parameters.",
                             "Highest capacity."]),
]
for i, (n, h_, b_) in enumerate(models):
    card(s, 0.7 + i * (cw + 0.22), cy, cw, ch, h_, b_, number=n)
callout(s, 0.7, 5.5, 11.93, 1.0,
        "All trained with Adam, sparse categorical cross-entropy, early stopping and LR-reduction on plateau. "
        "Two-stage transfer: freeze the backbone to train the head, then fine-tune the top ~30%.",
        fill=CARD_BG2, text_color=NAVY, size=13)
notes(s, "Contrast the from-scratch baseline with the two transfer-learning models and the two-stage protocol. ~40s.")

# ======================================================================
# Slide 7 — Training behaviour
# ======================================================================
s = slide()
header(s, "Training Behaviour", "Convergence and overfitting control",
       "Accuracy and loss, training versus validation")
figure(s, "training_curves.png", 0.7, 2.05, 7.4, 4.6)
tf = textbox(s, 8.35, 2.3, 4.3, 4.2, anchor=MSO_ANCHOR.TOP)
para(tf, "What the curves show", 18, NAVY, bold=True, first=True, space_after=8)
for b in ["All models converge within the epoch budget.",
          "Early stopping restores the best validation weights.",
          "The small train–validation gap shows augmentation kept overfitting under control.",
          "Transfer-learning models start higher and plateau sooner than the from-scratch baseline."]:
    para(tf, b, 14, INK, bullet="•", space_after=8)
notes(s, "Read the training curves: convergence, early stopping, and the train-val gap as an overfitting check. ~35s.")

# ======================================================================
# Slide 8 — Results table
# ======================================================================
s = slide()
header(s, "Results — Test Set", "Accuracy, and the cost of chasing it",
       "Headline metrics on the 500-image held-out test set")
rows = [
    ("Model", "Accuracy", "Macro-F1", "Top-3", "Inference", "Size"),
    ("Custom CNN", "0.813", "0.796", "0.921", "3.4 ms", "4.9 MB"),
    ("EfficientNetV2-B0  ✓", "0.910", "0.895", "0.974", "4.8 ms", "38 MB"),
    ("ConvNeXt-Tiny", "0.891", "0.880", "0.962", "12.9 ms", "235 MB"),
]
nrows, ncols = len(rows), len(rows[0])
tbl_w, tbl_h = 11.93, 2.45
gx = s.shapes.add_table(nrows, ncols, Inches(0.7), Inches(2.0),
                        Inches(tbl_w), Inches(tbl_h)).table
widths = [3.4, 1.75, 1.65, 1.45, 1.78, 1.9]
for j, wd in enumerate(widths):
    gx.columns[j].width = Inches(wd * tbl_w / sum(widths))
gx.first_row = True
for j in range(ncols):
    c = gx.cell(0, j)
    c.fill.solid(); c.fill.fore_color.rgb = NAVY
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = c.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
    r = p.add_run(); r.text = rows[0][j]; _set(r, 14, WHITE, bold=True)
for i in range(1, nrows):
    best = "✓" in rows[i][0]
    for j in range(ncols):
        c = gx.cell(i, j)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG2 if (i % 2 == 0) else WHITE
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = c.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        r = p.add_run(); r.text = rows[i][j]
        _set(r, 13.5, NAVY if best else INK, bold=(best and (j == 0 or j == 1)))
# two callouts
callout(s, 0.7, 4.85, 5.85, 1.6,
        "Both pretrained backbones beat the from-scratch baseline by roughly 8–10 accuracy points, "
        "answering RQ1 and RQ2.", fill=DARKCARD, text_color=WHITE, icon="✓",
        title="Transfer learning wins", size=13)
callout(s, 6.78, 4.85, 5.85, 1.6,
        "EfficientNetV2-B0 matches the top accuracy at a fraction of ConvNeXt-Tiny's size and latency — "
        "the best balance for deployment (RQ4).", fill=CARD_BG, text_color=NAVY, icon="⚡",
        title="Efficiency matters", size=13)
notes(s, REPLACE + " After the run, set the ✓ on whichever model gives the best "
         "accuracy/size/speed balance and update every number in this table. ~50s.")

# ======================================================================
# Slide 9 — Class-level analysis
# ======================================================================
s = slide()
header(s, "Class-level Analysis", "Where the mistakes land",
       "A 100 x 100 confusion matrix")
figure(s, "confusion_matrix.png", 0.7, 2.05, 7.2, 4.6)
tf = textbox(s, 8.15, 2.3, 4.5, 4.2)
para(tf, "Reading the errors", 18, NAVY, bold=True, first=True, space_after=8)
for b in ["A strong diagonal: most classes are recognised reliably.",
          "Errors concentrate between visually similar sports — e.g. bowling vs bocce, or related racquet sports.",
          "Distinctive-scene sports (e.g. swimming, motor racing) are near-perfect.",
          "This pattern is exactly what explainability then probes (RQ3)."]:
    para(tf, b, 14, INK, bullet="•", space_after=8)
notes(s, "Use the confusion matrix to name the hardest, most-confused sports and the easiest ones. ~35s.")

# ======================================================================
# Slide 10 — Explainability
# ======================================================================
s = slide()
header(s, "Explainability", "Does the model look at the right thing?",
       "Two independent methods: Grad-CAM and SHAP")
figure(s, "gradcam.png", 0.7, 2.05, 5.85, 3.0, "Grad-CAM — class activation heatmaps")
figure(s, "shap.png", 6.78, 2.05, 5.85, 3.0, "SHAP — pixel-level attributions")
callout(s, 0.7, 5.55, 5.85, 1.4,
        "Both methods are computed independently yet highlight the athlete, ball and playing area — "
        "strengthening trust that predictions use meaningful features (RQ3).",
        fill=GREEN_BG, text_color=GREEN_TX, icon="✓", title="Methods agree", size=12.5)
callout(s, 6.78, 5.55, 5.85, 1.4,
        "On some errors the attention drifts to the background — a reliability warning that explainability "
        "surfaces and accuracy alone hides.",
        fill=RED_BG, text_color=RED_TX, icon="✕", title="But not always", size=12.5)
notes(s, "Show Grad-CAM and SHAP agree on correct cases and expose background reliance on wrong ones. ~45s.")

# ======================================================================
# Slide 11 — Efficiency & deployment
# ======================================================================
s = slide()
header(s, "Trade-off & Deployment", "Choosing for balance, not for the leaderboard",
       "Accuracy is only one axis")
cw, cy, ch = 3.82, 2.1, 2.5
trade = [
    ("Custom CNN", ["4.9 MB · 3.4 ms.", "Smallest and fastest; best where compute is tight."]),
    ("EfficientNetV2-B0", ["38 MB · 4.8 ms.", "Top accuracy, compact, fast.", "Selected for deployment."]),
    ("ConvNeXt-Tiny", ["235 MB · 12.9 ms.", "Highest capacity, but ~6x larger and slower for marginal gains."]),
]
for i, (h_, b_) in enumerate(trade):
    fill = DARKCARD if i == 1 else CARD_BG
    hc = WHITE if i == 1 else NAVY
    bc = WHITE if i == 1 else INK
    card(s, 0.7 + i * (cw + 0.22), cy, cw, ch, h_, b_, fill=fill, head_color=hc, body_color=bc)
callout(s, 0.7, 4.95, 11.93, 1.45,
        "Deployed on Hugging Face Spaces with Gradio: upload an image and get the top-5 sports, "
        "confidence scores, and a live Grad-CAM heatmap — directly in the browser (RQ4 & RQ5).",
        fill=CARD_BG2, text_color=NAVY, icon="🚀", title="Live, explainable web demo")
notes(s, "Argue for balance over raw accuracy; introduce the live demo (you will show it in the 2-min demo part). ~40s.")

# ======================================================================
# Slide 12 — Conclusion
# ======================================================================
s = slide()
header(s, "Conclusion", "Accuracy is necessary. Explanation makes it trustworthy.",
       "What the study established")
points = [
    ("Strong results", "All three CNNs classify 100 sports well; the best exceeds ~91% test accuracy."),
    ("Transfer learning wins", "ImageNet pretraining beats the from-scratch baseline by a wide margin (RQ1, RQ2)."),
    ("Explanations validated", "Grad-CAM and SHAP confirm focus on athletes and equipment — and expose occasional background reliance (RQ3)."),
    ("Deployed prototype", "EfficientNetV2-B0 chosen for balance and shipped as an explainable web demo (RQ4, RQ5)."),
]
y = 2.05
for h_, b_ in points:
    # arrow
    ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(0.7), Inches(y + 0.08), Inches(0.7), Inches(0.42))
    ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT; ar.line.fill.background(); ar.shadow.inherit = False
    tf = textbox(s, 1.6, y, 11.0, 0.95)
    para(tf, h_, 17, NAVY, bold=True, first=True, space_after=2)
    para(tf, b_, 14, INK, space_after=0)
    y += 0.97
callout(s, 0.7, 6.0, 11.93, 1.2,
        "Single public dataset, no external validation, and heatmaps are not proof of correct reasoning. "
        "Future work: add diverse external data and reduce background-shortcut behaviour.",
        fill=CARD_BG2, text_color=NAVY, icon="🔭", title="Limitations & future work", size=12.5)
notes(s, "Summarise the four takeaways, state limitations honestly, and thank the audience. ~40s.")

# ----------------------------------------------------------------------
out = os.path.join(HERE, "sports_cnn_presentation.pptx")
prs.save(out)
print("wrote", out, "—", len(prs.slides._sldIdLst), "slides")
