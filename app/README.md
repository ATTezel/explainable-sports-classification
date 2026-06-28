---
title: Explainable Sports Classifier
emoji: 🏅
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
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
1. Create an account at https://huggingface.co → **New Space** → SDK **Gradio**.
2. Upload `app.py`, `requirements.txt`, `best_model.keras`, `class_names.json` (this `README.md`
   header configures the Space).
3. The Space builds automatically and gives you a public URL — paste it into the report and Teams
   submission as the **web link for the interface**.

> Tip: `best_model.keras` can be large. If the Space build is slow, use Git LFS or host the model on
> the Hugging Face Hub and load it with `huggingface_hub.hf_hub_download`.

## Alternative: Streamlit / Vercel
The same `predict()` logic works in a Streamlit app (`st.file_uploader` → `st.image`). For a
Vercel-hosted client like the plant-disease example, deploy the model behind a small inference API
(e.g., this Gradio app exposes a REST endpoint at `/api/predict`) and call it from a static frontend.
