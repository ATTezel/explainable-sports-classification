#!/usr/bin/env python3
"""Generates workflow.png — the methodology pipeline figure for the report.
Run with the matplotlib-enabled interpreter:
    ~/homework/Assignment3-Classifiers/.venv/bin/python make_workflow.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

STEPS = [
    ("1", "Data\nCollection", "#2563eb", ["1.1 100 Sports\n(100 classes)", "1.2 train/valid/test\n13,493/500/500"]),
    ("2", "Preprocess &\nAugment",  "#0891b2", ["2.1 Resize 224x224", "2.2 Flip/Rotate\nZoom/Contrast"]),
    ("3", "Model\nDevelopment",     "#7c3aed", ["3.1 Custom CNN", "3.2 EfficientNetV2-B0", "3.3 ConvNeXt-Tiny"]),
    ("4", "Training",               "#db2777", ["4.1 Adam + SCCE", "4.2 Two-stage TL", "4.3 Early stopping"]),
    ("5", "Evaluation",             "#ea580c", ["5.1 Acc / Top-k / F1", "5.2 Confusion matrix", "5.3 Efficiency"]),
    ("6", "Explainability",         "#16a34a", ["6.1 Grad-CAM", "6.2 SHAP"]),
    ("7", "Deployment",             "#475569", ["7.1 Gradio web app"]),
]

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, len(STEPS) * 2.3)
ax.set_ylim(0, 10)
ax.axis("off")
fig.patch.set_facecolor("white")

R = 0.62
y_circle = 7.6
for i, (num, title, color, subs) in enumerate(STEPS):
    cx = i * 2.3 + 1.15
    # numbered circle
    ax.add_patch(Circle((cx, y_circle), R, facecolor=color, edgecolor="white", lw=2, zorder=3))
    ax.text(cx, y_circle, num, ha="center", va="center", color="white",
            fontsize=20, fontweight="bold", zorder=4)
    ax.text(cx, y_circle - R - 0.45, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color="#111827")
    # arrow to next step
    if i < len(STEPS) - 1:
        nx = (i + 1) * 2.3 + 1.15
        ax.add_patch(FancyArrowPatch((cx + R + 0.1, y_circle), (nx - R - 0.1, y_circle),
                                     arrowstyle="-|>", mutation_scale=22, lw=2.4,
                                     color="#9ca3af", zorder=2))
    # substep box
    box_h = 0.55 * len(subs) + 0.5
    box_y = 4.7 - box_h
    box = FancyBboxPatch((cx - 1.0, box_y), 2.0, box_h,
                         boxstyle="round,pad=0.06,rounding_size=0.12",
                         facecolor=color, alpha=0.10, edgecolor=color, lw=1.6, zorder=1)
    ax.add_patch(box)
    for j, s in enumerate(subs):
        ax.text(cx, box_y + box_h - 0.45 - j * 0.55, s, ha="center", va="center",
                fontsize=8.0, color="#1f2937")
    # connector from circle to its substep box
    ax.add_patch(FancyArrowPatch((cx, y_circle - R - 0.95), (cx, 4.75),
                                 arrowstyle="-|>", mutation_scale=13, lw=1.3,
                                 color=color, zorder=2))

ax.text(len(STEPS) * 1.15, 9.4,
        "Explainable Sports Category Classification — Methodology Pipeline",
        ha="center", va="center", fontsize=15, fontweight="bold", color="#0f172a")
ax.text(len(STEPS) * 1.15, 0.7,
        "Custom CNN  vs.  EfficientNetV2-B0  vs.  ConvNeXt-Tiny   +   Grad-CAM & SHAP   +   Web deployment",
        ha="center", va="center", fontsize=10.5, style="italic", color="#475569")

plt.tight_layout()
out = __file__.rsplit("/", 1)[0] + "/workflow.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
print("wrote", out)
