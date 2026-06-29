---
title: Explainable Sports Classifier
emoji: 🏅
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.50.0
python_version: "3.12"
app_file: app.py
pinned: false
---

# Explainable Sports Category Classifier — web demo

Gradio front-end for the *Machine Learning & Smart Systems* project (Topic 12.4). Upload a sports
image; the model returns the **top-5 sports categories** and a **Grad-CAM** heatmap of the regions
that drove the prediction.

## Files needed next to `app.py`
Both come from the Kaggle notebook output (`/kaggle/working`):
- `best_model.keras` — the best-performing trained model (from `models/`).
- `class_names.json` — the ordered list of the 100 class names.

## Run locally
```bash
pip install -r requirements.txt
python app.py        # opens http://127.0.0.1:7860
```

## Deploy on Hugging Face Spaces (free, recommended)

> Verified: smoke-tested locally on the pinned stack (TensorFlow 2.19 + Gradio 5.50, Python 3.12) —
> the model loads, `predict()` returns the top-5 plus a Grad-CAM overlay, and `get_api_info()` +
> `launch()` start cleanly. Keep the pins: a Keras-3 `.keras` will not load on TF ≤ 2.15, and the
> gradio 4.44 line crashed on launch with a json-schema bug.

**Option A — one command (recommended).** Get a *write* token at
https://huggingface.co/settings/tokens, then:
```bash
cd app
HF_USER=<your-hf-username> HF_TOKEN=hf_xxx bash deploy_to_hf.sh
```
It creates the Space, uploads all five files (the 248 MB model goes via LFS automatically), and prints
the public URL.

**Option B — web UI.** https://huggingface.co → **New Space** → SDK **Gradio** → upload `app.py`,
`requirements.txt`, `README.md`, `class_names.json`, and `best_model.keras` (this `README.md` header
configures the Space).

Either way you get a public URL like `https://huggingface.co/spaces/<you>/explainable-sports-classifier`
— paste it into the report and the Teams submission as the **web link for the interface**. The build
takes a few minutes (the 248 MB model takes a moment to load on first request).

## Alternative: Streamlit / Vercel
The same `predict()` logic works in a Streamlit app (`st.file_uploader` → `st.image`). For a
Vercel-hosted client like the plant-disease example, deploy the model behind a small inference API
(e.g., this Gradio app exposes a REST endpoint at `/api/predict`) and call it from a static frontend.
