"""Explainable Sports Category Classifier — Gradio web app.

Loads the best model exported by the Kaggle notebook (`best_model.keras` + `class_names.json`),
predicts the top-5 sports categories for an uploaded image, and shows a Grad-CAM heatmap of the
regions that drove the prediction.

Run locally:   pip install -r requirements.txt && python app.py
Deploy:        push this folder to a Hugging Face Space (SDK = Gradio). See README.md.
"""
import json
import os

import gradio as gr
from matplotlib import colormaps
import numpy as np
import tensorflow as tf
from tensorflow import keras

IMG_SIZE = 224
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "best_model.keras")
CLASSES_PATH = os.path.join(HERE, "class_names.json")

# ---------------------------------------------------------------- load artifacts
model, class_names, LOAD_ERROR = None, None, None
try:
    model = keras.models.load_model(MODEL_PATH)
    with open(CLASSES_PATH) as f:
        class_names = json.load(f)
except Exception as e:  # noqa: BLE001
    LOAD_ERROR = (
        f"Could not load model artifacts ({type(e).__name__}: {e}).\n"
        "Download `best_model.keras` (Output > models/) and `class_names.json` from the Kaggle "
        "run and place them next to app.py."
    )


def _last_conv_layer_name(m):
    for layer in reversed(m.layers):
        try:
            if len(layer.output.shape) == 4:
                return layer.name
        except Exception:  # noqa: BLE001
            continue
    return None


def _gradcam(img_batch, pred_index):
    last_conv = _last_conv_layer_name(model)
    grad_model = keras.Model(model.inputs, [model.get_layer(last_conv).output, model.output])
    with tf.GradientTape() as tape:
        conv_out, preds = grad_model(img_batch)
        channel = preds[:, pred_index]
    grads = tape.gradient(channel, conv_out)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    heat = tf.squeeze(conv_out[0] @ pooled[..., tf.newaxis])
    heat = tf.maximum(heat, 0) / (tf.reduce_max(heat) + 1e-8)
    heat = tf.image.resize(heat[..., None], (IMG_SIZE, IMG_SIZE)).numpy()[..., 0]
    return heat


def predict(image):
    if model is None:
        raise gr.Error(LOAD_ERROR)
    if image is None:
        return {}, None
    img = tf.image.resize(image, (IMG_SIZE, IMG_SIZE)).numpy().astype("float32")
    batch = img[None]
    probs = model.predict(batch, verbose=0)[0]
    top = probs.argsort()[-5:][::-1]
    labels = {class_names[i]: float(probs[i]) for i in top}

    heat = _gradcam(batch, int(top[0]))
    jet = colormaps["jet"](heat)[..., :3]
    overlay = np.clip(0.55 * (img / 255.0) + 0.45 * jet, 0, 1)
    return labels, (overlay * 255).astype("uint8")


title = "🏅 Explainable Sports Category Classifier"
description = (
    "Upload a sports image. The model (best of Custom CNN / EfficientNetV2-B0 / ConvNeXt-Tiny, "
    "trained on the 100 Sports dataset) returns the top-5 categories and a **Grad-CAM** heatmap "
    "showing which regions drove the prediction. Built for the Machine Learning & Smart Systems "
    "project (Topic 12.4)."
)

demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="numpy", label="Sports image"),
    outputs=[gr.Label(num_top_classes=5, label="Top-5 prediction"),
             gr.Image(label="Grad-CAM explanation")],
    title=title,
    description=description,
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
