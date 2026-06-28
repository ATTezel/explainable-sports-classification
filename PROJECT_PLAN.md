# Project Plan — 12.4 Explainable Sports Category Classification

**Student:** Arda Tekin Tezel · arda.t.tezel@gmail.com
**Module:** Machine Learning & Smart Systems — CNN-Based Image Dataset Research Project
**Due:** 3 July 2026, 23:59

---

## 1. Canonical project facts (keep identical everywhere — notebook, report, slides, app)

| Item | Value |
|---|---|
| **Title** | Explainable Sports Category Classification Using CNN Transfer Learning: A Comparative Study of a Custom CNN, EfficientNetV2, and ConvNeXt-Tiny with Grad-CAM and SHAP |
| **Task** | Multi-class image classification (sports category from a still image) |
| **Dataset** | *100 Sports Image Classification* — Kaggle, `gpiosenka/sports-classification` |
| **Classes** | 100 sports categories |
| **Size** | ~13,493 train + 500 valid + 500 test (≈14,493 images), 224×224×3 JPG |
| **Models** | (1) Custom CNN baseline · (2) EfficientNetV2-B0 (TL) · (3) ConvNeXt-Tiny (TL) |
| **XAI** | Grad-CAM (region heatmaps) + SHAP (pixel/region attribution) |
| **Framework** | TensorFlow / Keras (Kaggle GPU) |
| **Deployment** | Gradio web app (deployable free on Hugging Face Spaces) |
| **Metrics** | accuracy, top-3, top-5, macro precision/recall/F1, weighted F1, confusion matrix, per-class F1, params, model size (MB), train time, inference ms/img |

### Research Questions (from the template's sample figure for this exact topic)
- **RQ1** — Which model best classifies sports categories from image data?
- **RQ2** — Does transfer learning improve recognition compared with a custom CNN?
- **RQ3** — Do Grad-CAM and SHAP explanations focus on sport-relevant regions (athletes, equipment, court/pitch) rather than background shortcuts?
- **RQ4** — Which model gives the best trade-off between classification performance, inference speed, and model size?
- **RQ5** — Can the best model be deployed as an explainable web-based sports-image classification prototype?

---

## 2. The three phases (from the assignment brief)

- **Phase 1 — Topic Selection (20 pts):** done in class. Topic 12.4 chosen.
- **Phase 2 — Technical Implementation (30 pts):** Kaggle notebook → run → results → front-end → public GitHub.
- **Phase 3 — Report + Presentation (50 pts):** Overleaf report (PDF + share link) + presentation video + web link + GitHub link + Kaggle link.

---

## 3. What I (Claude) prepare vs. what you (Arda) must do

### Prepared for you (in this folder)
1. `notebook/sports_cnn_explainable.ipynb` — single Kaggle-ready notebook. Trains all 3 models, evaluates, runs Grad-CAM + SHAP, and **auto-exports `results.json` + every figure** the report needs, then zips them.
2. `app/app.py` — Gradio front-end (+ `requirements.txt`, deploy README).
3. `report/main.tex` + `report/references.bib` — full Overleaf report, ~95% complete; only the **real numbers/figures from your Kaggle run** get slotted in.
4. `slides/` — presentation outline + spoken video script.
5. `README.md` — public GitHub README + exact push commands.
6. This `PROJECT_PLAN.md`.

### You must do (needs your accounts — I cannot)
- [ ] **Run the notebook on Kaggle** (GPU on): add the dataset, Run All, download `results.zip` from `/kaggle/working`. Send me the zip → I fill the report's real numbers/figures. *(I will not fabricate results — the brief requires "results must match the code".)*
- [ ] **Overleaf:** open template → *Menu → Copy Project* → paste `main.tex` + `references.bib` → upload figures from `results.zip` → *Share → Anyone with link can view* → copy link.
- [ ] **GitHub:** create a public repo, run the push commands in `README.md` → copy repo link.
- [ ] **Deploy the app:** push `app/` to a Hugging Face Space (Gradio SDK) → copy web link. *(See `app/README.md`.)*
- [ ] **Record the video** using `slides/video_script.md`.

---

## 4. Execution order (fastest path to submission)

1. **Kaggle run** (longest pole, ~30–60 min GPU). Start this first.
2. While it runs: open the Overleaf copy, paste `main.tex`/`references.bib`.
3. When the run finishes: upload figures, send me `results.zip`, I finalize numbers.
4. Deploy Gradio app, grab web link.
5. Record video from slides + the deployed app.
6. Submit on Teams: Overleaf link · final PDF · video · web link · GitHub link · Kaggle link.

---

## 5. Integrity notes
- All references in the report are **real, verified** peer-reviewed papers (gathered via live search, not invented).
- Results tables in `main.tex` carry clearly-marked placeholders until the real Kaggle numbers replace them.
- The notebook is deterministic-seeded so reruns are reproducible.
