# Presentation slides — outline (12 slides, ~8 min) — plus a ~2 min live demo first = ~10 min video

Build these in PowerPoint/Google Slides. Each slide lists its title and the key visuals/bullets.
Pull every figure from `results.zip` (the Kaggle run). Keep it clean: white background, one idea per slide.

---

**1 — Title**
- *Explainable Sports Category Classification Using CNN Transfer Learning*
- Custom CNN vs. EfficientNetV2-B0 vs. ConvNeXt-Tiny · Grad-CAM + SHAP · Web demo
- Arda Tekin Tezel · ML & Smart Systems · Topic 12.4

**2 — Problem & motivation**
- Sports media/archives need automatic tagging of images by sport.
- Manual tagging is slow, costly, inconsistent at scale.
- Goal: an accurate **and explainable** 100-class sports image classifier.

**3 — Dataset**
- 100 Sports Image Classification (Kaggle, gpiosenka): 100 classes, 13,493 / 500 / 500.
- Show `sample_grid.png` + `class_distribution.png`.

**4 — Research questions (RQ1–RQ5)**
- One line each (best model, transfer vs custom, do explanations look at the right regions, accuracy/speed/size trade-off, deployable prototype).

**5 — Methodology pipeline**
- Workflow figure: data → preprocess/augment → 3 models → evaluate → Grad-CAM/SHAP → deploy.
- Note: 224×224, augmentation (h-flip/rotate/zoom/contrast), Adam, early stopping, seed 42.

**6 — Models**
- Custom CNN (4 conv blocks) · EfficientNetV2-B0 (TL) · ConvNeXt-Tiny (TL).
- Two-stage transfer: freeze backbone → fine-tune top ~30%.

**7 — Training behaviour**
- Show `training_curves.png` (accuracy/loss, train vs val) — convergence, early stopping, overfitting check.

**8 — Results: model comparison**
- Show the main results table (acc, macro-F1, top-3, params, size, inference); `model_comparison.png` optional.
- State the best model (RQ1) and the transfer-vs-custom gap (RQ2).

**9 — Class-level analysis**
- Show `confusion_matrix.png`; name best/worst classes and most-confused visually-similar sports (RQ3).

**10 — Explainability: Grad-CAM + SHAP**
- Show `gradcam.png` and `shap.png`.
- Do heatmaps fall on athletes/equipment/court, not background? (RQ3) — agreement between methods.

**11 — Efficiency & web demo**
- Accuracy–efficiency trade-off (RQ4); show the deployed Gradio app screenshot/URL (RQ5).

**12 — Limitations, conclusion, links**
- Single dataset, no external validation, heatmaps ≠ proof of reasoning, class imbalance.
- Conclusion: best model + key takeaway.
- Links: GitHub · Kaggle · Overleaf · live app.
