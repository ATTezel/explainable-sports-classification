# Explainable Sports Category Classification Using CNN Transfer Learning

A comparative, **explainable** image-classification study that recognizes the **sport category** of a
still image across **100 sports classes**, comparing a **Custom CNN** baseline against two
ImageNet-pretrained backbones — **EfficientNetV2-B0** and **ConvNeXt-Tiny** — and interpreting the
best model with **Grad-CAM** and **SHAP**. Built for the *Machine Learning & Smart Systems* module
project (Topic **12.4 — Explainable Sports Category Classification**).

> **Author:** Arda Tekin Tezel · University of Europe for Applied Sciences

---

## Research questions
- **RQ1** — Which model best classifies sports categories from image data?
- **RQ2** — Does transfer learning improve recognition compared with a custom CNN?
- **RQ3** — Do Grad-CAM and SHAP explanations focus on sport-relevant regions (athletes, equipment, court/pitch) rather than background shortcuts?
- **RQ4** — Which model gives the best trade-off between classification performance, inference speed, and model size?
- **RQ5** — Can the best model be deployed as an explainable web-based sports-image classification prototype?

## Dataset
[**100 Sports Image Classification**](https://www.kaggle.com/datasets/gpiosenka/sports-classification)
(Kaggle, `gpiosenka/sports-classification`) — 100 classes, **13,493 train + 500 valid + 500 test**
images (5 valid + 5 test per class), all **224×224×3 JPG**.

## Repository structure
```
ML-Project-Sports-CNN/
├── notebook/
│   ├── sports_cnn_explainable.ipynb   # Kaggle-ready: trains 3 models, evaluates, Grad-CAM + SHAP,
│   │                                  #   exports results.json + figures, zips them
│   └── build_notebook.py              # regenerates the .ipynb from source
├── app/
│   ├── app.py                         # Gradio web demo (top-5 + Grad-CAM)
│   ├── requirements.txt
│   └── README.md                      # Hugging Face Spaces deploy guide
├── report/
│   ├── main.tex                       # Overleaf (elsarticle) research report
│   ├── references.bib                 # 39 verified references
│   ├── sections/                      # report body (\input into main.tex)
│   └── figures/                       # drop results.zip figures here
├── slides/                            # presentation outline + video script
├── PROJECT_PLAN.md
└── README.md
```

## Reproduce (Phase 2)
1. Open [Kaggle](https://www.kaggle.com) → **New Notebook** → upload `notebook/sports_cnn_explainable.ipynb`.
2. **Add Input** → search *"100 Sports Image Classification"* (gpiosenka) → add it.
3. Settings → **Accelerator: GPU** (T4/P100), Internet **On** (for ImageNet weights).
4. **Run All**. Runtime ≈ 30–60 min.
5. From the **Output** panel download `results.zip` (all figures + `results.json`) and `models/best_model.keras`.
6. Drop the figures into the report: from the repo root run `cd report && unzip -o /path/to/results.zip`. The archive already contains a `figures/` folder, so the PNGs land at `report/figures/*.png`. (Do **not** unzip *inside* `report/figures/`, or they nest as `figures/figures/` and the report shows placeholders.)

## Run the web app (Phase 2 front-end)
```bash
cd app
# place best_model.keras and class_names.json (from the Kaggle output) next to app.py
pip install -r requirements.txt
python app.py
```
Deploy free on Hugging Face Spaces — see [`app/README.md`](app/README.md).

## Tech stack
Python · TensorFlow/Keras · scikit-learn · SHAP · Matplotlib · Gradio · Kaggle GPU

## Models
| Model | Role | Pretraining |
|---|---|---|
| Custom CNN | baseline | trained from scratch |
| EfficientNetV2-B0 | transfer learning | ImageNet |
| ConvNeXt-Tiny | transfer learning | ImageNet |

## Project links
- **GitHub repo:** https://github.com/ATTezel/explainable-sports-classification
- **Kaggle notebook:** https://www.kaggle.com/code/ardatezel/explainable-sports-classification
- **Overleaf report:** _add share link_
- **Live web app (HF Space):** _add after deploy_
- **Presentation video:** _add link_

---

## Repository
This project is public at **https://github.com/ATTezel/explainable-sports-classification**.
Clone it with:
```bash
git clone https://github.com/ATTezel/explainable-sports-classification.git
```

> **Results (from the executed Kaggle run):** the report's tables and figures are populated from
> `results.json` and the 7 exported figures. Best model: **ConvNeXt-Tiny** (96.4% test accuracy,
> 0.963 macro-F1), deployed as the prototype; **EfficientNetV2-B0** is the recommended efficiency
> trade-off (96.2% accuracy at ~1/5 the size and ~1/12 the latency); the from-scratch custom CNN
> baseline reaches 47.2%, so transfer learning improves accuracy by ~49 points.
