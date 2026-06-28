#!/usr/bin/env python3
"""Builds sports_cnn_explainable.ipynb (Kaggle-ready) from raw cell sources.
No nbformat dependency: emits nbformat v4 JSON directly.
Run:  python3 build_notebook.py
"""
import json, os

cells = []  # list of ("md"|"code", source_string)


def md(s):  cells.append(("md", s.strip("\n")))
def code(s): cells.append(("code", s.strip("\n")))


# ---------------------------------------------------------------- 0. Title
md(r"""
# Explainable Sports Category Classification Using CNN Transfer Learning
**Custom CNN vs. EfficientNetV2-B0 vs. ConvNeXt-Tiny · Grad-CAM + SHAP · Web Deployment**

Author: Arda Tekin Tezel — Machine Learning & Smart Systems project (Topic 12.4)

**Dataset:** [100 Sports Image Classification](https://www.kaggle.com/datasets/gpiosenka/sports-classification) (100 classes, ~14.5k images).
Add it to this notebook via *Add Input* and turn the **GPU** accelerator on, then *Run All*.

This notebook is self-contained: it trains three models, evaluates them, generates Grad-CAM and
SHAP explanations, and writes every figure plus `results.json` into `/kaggle/working`, finally
zipping them as `results.zip` for the report.
""")

# ---------------------------------------------------------------- 1. Setup
md("## 0. Environment & configuration")

code(r"""
# SHAP is usually preinstalled on Kaggle; install quietly if missing.
import importlib, subprocess, sys
if importlib.util.find_spec('shap') is None:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'shap'], check=False)
""")

code(r"""
import os, glob, json, time, random, zipfile, collections, warnings
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

SEED = 42
random.seed(SEED); np.random.seed(SEED); tf.random.set_seed(SEED)

IMG_SIZE   = 224
BATCH_SIZE = 32
AUTOTUNE   = tf.data.AUTOTUNE

# Epoch budget. Set FAST_RUN=True for a quick smoke test, then flip back to False for the real run.
FAST_RUN        = False
EPOCHS_CUSTOM   = 30 if not FAST_RUN else 2   # custom CNN trains from scratch -> needs more
EPOCHS_HEAD     = 8  if not FAST_RUN else 1   # frozen-backbone (transfer) head training
EPOCHS_FINETUNE = 8  if not FAST_RUN else 1   # fine-tuning unfrozen top of backbone

OUT_DIR   = '/kaggle/working'
FIG_DIR   = os.path.join(OUT_DIR, 'figures');  os.makedirs(FIG_DIR, exist_ok=True)
MODEL_DIR = os.path.join(OUT_DIR, 'models');   os.makedirs(MODEL_DIR, exist_ok=True)

print('TensorFlow', tf.__version__)
print('GPU devices:', tf.config.list_physical_devices('GPU'))
""")

# ---------------------------------------------------------------- 2. Dataset
md(r"""
## 1. Dataset loading

The 100 Sports dataset already ships with `train/`, `valid/`, and `test/` folders, each holding one
sub-folder per class. We auto-detect the dataset root under `/kaggle/input` so the notebook works
regardless of the exact mount name.
""")

code(r"""
DATA_ROOT = None
for d in sorted(glob.glob('/kaggle/input/*')):
    if os.path.isdir(os.path.join(d, 'train')):
        DATA_ROOT = d; break
assert DATA_ROOT, 'No dataset with a train/ folder found under /kaggle/input. Use "Add Input" to attach the 100 Sports dataset.'

TRAIN_DIR = os.path.join(DATA_ROOT, 'train')
VALID_DIR = os.path.join(DATA_ROOT, 'valid') if os.path.isdir(os.path.join(DATA_ROOT, 'valid')) else os.path.join(DATA_ROOT, 'test')
TEST_DIR  = os.path.join(DATA_ROOT, 'test')  if os.path.isdir(os.path.join(DATA_ROOT, 'test'))  else VALID_DIR
print('DATA_ROOT :', DATA_ROOT)
print('train/valid/test ->', TRAIN_DIR, VALID_DIR, TEST_DIR, sep='\n  ')
""")

code(r"""
train_ds_raw = keras.utils.image_dataset_from_directory(
    TRAIN_DIR, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE,
    label_mode='int', shuffle=True, seed=SEED)
class_names = train_ds_raw.class_names
NUM_CLASSES = len(class_names)

val_ds_raw  = keras.utils.image_dataset_from_directory(
    VALID_DIR, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE,
    label_mode='int', shuffle=False)
test_ds_raw = keras.utils.image_dataset_from_directory(
    TEST_DIR, image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE,
    label_mode='int', shuffle=False)

train_ds = train_ds_raw.prefetch(AUTOTUNE)
val_ds   = val_ds_raw.prefetch(AUTOTUNE)
test_ds  = test_ds_raw.prefetch(AUTOTUNE)
print('Classes:', NUM_CLASSES)
print('First 8 classes:', class_names[:8])
""")

# ---------------------------------------------------------------- 3. EDA
md("## 2. Dataset inspection & visualization")

code(r"""
# Per-class training image counts
counts = {c: len(os.listdir(os.path.join(TRAIN_DIR, c))) for c in class_names}
cnt_vals = np.array(list(counts.values()))
print('Train images:', int(cnt_vals.sum()))
print('Per class -> min %d | max %d | mean %.1f | std %.1f' % (cnt_vals.min(), cnt_vals.max(), cnt_vals.mean(), cnt_vals.std()))

n_val  = sum(len(os.listdir(os.path.join(VALID_DIR, c))) for c in os.listdir(VALID_DIR) if os.path.isdir(os.path.join(VALID_DIR, c)))
n_test = sum(len(os.listdir(os.path.join(TEST_DIR, c)))  for c in os.listdir(TEST_DIR)  if os.path.isdir(os.path.join(TEST_DIR, c)))

DATASET_STATS = dict(num_classes=NUM_CLASSES, n_train=int(cnt_vals.sum()), n_valid=int(n_val), n_test=int(n_test),
                     per_class_min=int(cnt_vals.min()), per_class_max=int(cnt_vals.max()),
                     per_class_mean=float(cnt_vals.mean()), per_class_std=float(cnt_vals.std()),
                     img_size=IMG_SIZE)
""")

code(r"""
# Class-distribution plot (sorted)
order = np.argsort(cnt_vals)
plt.figure(figsize=(12, 4))
plt.bar(range(NUM_CLASSES), cnt_vals[order], color='#3b6fb5')
plt.xlabel('class (sorted by count)'); plt.ylabel('train images')
plt.title('Per-class training image distribution (%d classes)' % NUM_CLASSES)
plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'class_distribution.png'), dpi=150); plt.show()
""")

code(r"""
# Sample grid: one image from each of 15 random classes
plt.figure(figsize=(13, 9))
sample_classes = random.sample(class_names, 15)
for i, c in enumerate(sample_classes):
    f = os.listdir(os.path.join(TRAIN_DIR, c))[0]
    img = keras.utils.load_img(os.path.join(TRAIN_DIR, c, f), target_size=(IMG_SIZE, IMG_SIZE))
    ax = plt.subplot(3, 5, i + 1); plt.imshow(img); plt.title(c, fontsize=9); plt.axis('off')
plt.suptitle('Sample images (one per class)'); plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'sample_grid.png'), dpi=150); plt.show()
""")

# ---------------------------------------------------------------- 4. Augmentation
md(r"""
## 3. Preprocessing & augmentation

Images are kept in `[0,255]` and each model applies its own `preprocess_input`, so the same
pipeline feeds all three networks. Augmentation is applied **inside** each model (active only at
training time). Horizontal flip is valid here because a sport's identity is invariant to left/right
mirroring; vertical flip is excluded because it produces physically implausible scenes.
""")

code(r"""
data_augmentation = keras.Sequential([
    layers.RandomFlip('horizontal'),
    layers.RandomRotation(0.08),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10),
], name='augment')
""")

# ---------------------------------------------------------------- 5. Models
md(r"""
## 4. Model development

- **Custom CNN** — a 4-block convolutional baseline trained from scratch.
- **EfficientNetV2-B0** and **ConvNeXt-Tiny** — ImageNet-pretrained backbones, trained in two stages
  (frozen-backbone head training, then fine-tuning the top ~30% of the backbone at a low learning rate).
""")

code(r"""
def build_custom_cnn():
    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1. / 255)(x)
    for f in [32, 64, 128, 256]:
        x = layers.Conv2D(f, 3, padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D()(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)
    return keras.Model(inputs, outputs, name='Custom_CNN')


def build_transfer(app_fn, preprocess_fn, name):
    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    x = data_augmentation(inputs)
    x = preprocess_fn(x)
    base = app_fn(include_top=False, weights='imagenet', input_tensor=x)
    base.trainable = False
    y = layers.GlobalAveragePooling2D()(base.output)
    y = layers.Dropout(0.3)(y)
    out = layers.Dense(NUM_CLASSES, activation='softmax')(y)
    return keras.Model(inputs, out, name=name), base
""")

code(r"""
def compile_model(model, lr=1e-3):
    model.compile(
        optimizer=keras.optimizers.Adam(lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy',
                 keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top3'),
                 keras.metrics.SparseTopKCategoricalAccuracy(k=5, name='top5')])
    return model


def train_model(model, epochs, lr=1e-3):
    compile_model(model, lr)
    cbs = [keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=4, restore_best_weights=True),
           keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6)]
    t0 = time.time()
    h = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=cbs, verbose=2)
    return h.history, time.time() - t0


def train_transfer(model, base, name):
    print('\n=== %s : stage 1 (frozen backbone) ===' % name)
    h1, t1 = train_model(model, EPOCHS_HEAD, lr=1e-3)
    base.trainable = True                       # stage 2: unfreeze top ~30%
    cut = int(len(base.layers) * 0.7)
    for l in base.layers[:cut]:
        l.trainable = False
    print('=== %s : stage 2 (fine-tune top %d layers) ===' % (name, len(base.layers) - cut))
    h2, t2 = train_model(model, EPOCHS_FINETUNE, lr=1e-5)
    merged = {k: h1.get(k, []) + h2.get(k, []) for k in set(h1) | set(h2)}
    return merged, t1 + t2
""")

code(r"""
histories, TRAIN_TIME, MODELS = {}, {}, {}

# 4.1 Custom CNN baseline
custom = build_custom_cnn(); custom.summary()
hist_c, t_c = train_model(custom, EPOCHS_CUSTOM)
histories['Custom_CNN'] = hist_c; TRAIN_TIME['Custom_CNN'] = t_c; MODELS['Custom_CNN'] = custom
""")

code(r"""
# 4.2 EfficientNetV2-B0 (transfer learning)
eff, eff_base = build_transfer(keras.applications.EfficientNetV2B0,
                               keras.applications.efficientnet_v2.preprocess_input, 'EfficientNetV2B0')
hist_e, t_e = train_transfer(eff, eff_base, 'EfficientNetV2B0')
histories['EfficientNetV2B0'] = hist_e; TRAIN_TIME['EfficientNetV2B0'] = t_e; MODELS['EfficientNetV2B0'] = eff
""")

code(r"""
# 4.3 ConvNeXt-Tiny (transfer learning)
cnx, cnx_base = build_transfer(keras.applications.ConvNeXtTiny,
                               keras.applications.convnext.preprocess_input, 'ConvNeXtTiny')
hist_x, t_x = train_transfer(cnx, cnx_base, 'ConvNeXtTiny')
histories['ConvNeXtTiny'] = hist_x; TRAIN_TIME['ConvNeXtTiny'] = t_x; MODELS['ConvNeXtTiny'] = cnx
""")

# ---------------------------------------------------------------- 6. Evaluation
md("## 5. Evaluation")

code(r"""
from sklearn.metrics import (classification_report, confusion_matrix,
                             precision_recall_fscore_support, accuracy_score, top_k_accuracy_score)

# Ground-truth labels for the test set (fixed order, shuffle=False)
y_true = np.concatenate([y.numpy() for _, y in test_ds_raw], axis=0)
all_labels = list(range(NUM_CLASSES))


def evaluate(model, name):
    probs = model.predict(test_ds, verbose=0)
    y_pred = probs.argmax(1)
    acc  = accuracy_score(y_true, y_pred)
    top3 = top_k_accuracy_score(y_true, probs, k=3, labels=all_labels)
    top5 = top_k_accuracy_score(y_true, probs, k=5, labels=all_labels)
    mp, mr, mf, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
    _, _, wf, _   = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    # Inference time (warm up, then time forward passes on one batch)
    batch = next(iter(test_ds))[0]
    _ = model(batch, training=False)
    t0 = time.time()
    for _ in range(5):
        _ = model(batch, training=False)
    inf_ms = (time.time() - t0) / (5 * batch.shape[0]) * 1000
    params = int(model.count_params())
    return dict(name=name, accuracy=float(acc), top3=float(top3), top5=float(top5),
                macro_precision=float(mp), macro_recall=float(mr), macro_f1=float(mf),
                weighted_f1=float(wf), inference_ms=float(inf_ms), params=params,
                model_size_mb=round(params * 4 / 1e6, 2),
                train_time_s=round(TRAIN_TIME[name], 1), probs=probs, y_pred=y_pred)


EVAL = {name: evaluate(m, name) for name, m in MODELS.items()}
for n, e in EVAL.items():
    print('%-18s acc=%.3f top3=%.3f top5=%.3f macroF1=%.3f params=%.1fM size=%.1fMB inf=%.2fms' %
          (n, e['accuracy'], e['top3'], e['top5'], e['macro_f1'], e['params'] / 1e6, e['model_size_mb'], e['inference_ms']))

BEST = max(EVAL, key=lambda k: EVAL[k]['macro_f1'])
print('\nBest model by macro-F1:', BEST)
""")

code(r"""
# Training & validation curves (accuracy + loss) for all models
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
for n, h in histories.items():
    if 'accuracy' in h:      axes[0].plot(h['accuracy'], label=n + ' train')
    if 'val_accuracy' in h:  axes[0].plot(h['val_accuracy'], '--', label=n + ' val')
    if 'loss' in h:          axes[1].plot(h['loss'], label=n + ' train')
    if 'val_loss' in h:      axes[1].plot(h['val_loss'], '--', label=n + ' val')
axes[0].set_title('Accuracy'); axes[0].set_xlabel('epoch'); axes[0].legend(fontsize=8)
axes[1].set_title('Loss');     axes[1].set_xlabel('epoch'); axes[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'training_curves.png'), dpi=150); plt.show()
""")

code(r"""
# Confusion matrix for the best model (100x100, row-normalized)
cm = confusion_matrix(y_true, EVAL[BEST]['y_pred'], labels=all_labels)
cm_norm = cm / np.clip(cm.sum(1, keepdims=True), 1, None)
plt.figure(figsize=(9, 8))
plt.imshow(cm_norm, cmap='viridis', vmin=0, vmax=1)
plt.colorbar(fraction=0.046); plt.title('Row-normalized confusion matrix — %s' % BEST)
plt.xlabel('predicted class'); plt.ylabel('true class')
plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'confusion_matrix.png'), dpi=150); plt.show()

# Most-confused class pairs (off-diagonal)
pairs = []
for i in range(NUM_CLASSES):
    for j in range(NUM_CLASSES):
        if i != j and cm[i, j] > 0:
            pairs.append((cm[i, j], class_names[i], class_names[j]))
pairs.sort(reverse=True)
TOP_CONFUSED = [{'true': t, 'pred': p, 'count': int(c)} for c, t, p in pairs[:10]]
print('Top confusions (true -> pred):')
for d in TOP_CONFUSED:
    print('  %2d  %s -> %s' % (d['count'], d['true'], d['pred']))
""")

code(r"""
# Per-class F1 (best model): best & worst classes
rep = classification_report(y_true, EVAL[BEST]['y_pred'], labels=all_labels,
                            target_names=class_names, output_dict=True, zero_division=0)
per_class_f1 = sorted(((class_names[i], rep[class_names[i]]['f1-score']) for i in range(NUM_CLASSES)),
                      key=lambda x: x[1])
WORST5 = [{'class': c, 'f1': round(f, 3)} for c, f in per_class_f1[:5]]
BEST5  = [{'class': c, 'f1': round(f, 3)} for c, f in per_class_f1[-5:][::-1]]
print('Worst 5 classes:', WORST5)
print('Best  5 classes:', BEST5)
""")

code(r"""
# Model comparison bar chart
names = list(EVAL.keys())
acc  = [EVAL[n]['accuracy'] for n in names]
f1   = [EVAL[n]['macro_f1'] for n in names]
x = np.arange(len(names)); w = 0.35
plt.figure(figsize=(7, 4.5))
plt.bar(x - w / 2, acc, w, label='accuracy', color='#3b6fb5')
plt.bar(x + w / 2, f1,  w, label='macro F1', color='#e07b39')
plt.xticks(x, names, rotation=10); plt.ylim(0, 1); plt.legend(); plt.title('Model comparison (test set)')
for i in range(len(names)):
    plt.text(x[i] - w / 2, acc[i] + 0.01, '%.2f' % acc[i], ha='center', fontsize=8)
    plt.text(x[i] + w / 2, f1[i] + 0.01, '%.2f' % f1[i], ha='center', fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'model_comparison.png'), dpi=150); plt.show()
""")

# ---------------------------------------------------------------- 7. Grad-CAM
md(r"""
## 6. Explainability — Grad-CAM

Grad-CAM highlights the image regions most responsible for the predicted class by weighting the last
convolutional feature maps with the gradient of the class score. We inspect correct high-confidence,
correct low-confidence, and misclassified examples for the best model.
""")

code(r"""
def last_conv_layer_name(model):
    for layer in reversed(model.layers):
        try:
            if len(layer.output.shape) == 4:
                return layer.name
        except Exception:
            continue
    return None


def make_gradcam_heatmap(img_batch, model, last_conv, pred_index=None):
    grad_model = keras.Model(model.inputs, [model.get_layer(last_conv).output, model.output])
    with tf.GradientTape() as tape:
        conv_out, preds = grad_model(img_batch)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    grads = tape.gradient(class_channel, conv_out)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_out[0]
    heat = conv_out @ pooled[..., tf.newaxis]
    heat = tf.squeeze(heat)
    heat = tf.maximum(heat, 0) / (tf.reduce_max(heat) + 1e-8)
    return heat.numpy()


def overlay(img_uint8, heat):
    import matplotlib.cm as cm
    heat_r = tf.image.resize(heat[..., None], (IMG_SIZE, IMG_SIZE)).numpy()[..., 0]
    jet = cm.get_cmap('jet')(heat_r)[..., :3]
    return np.clip(0.55 * (img_uint8 / 255.0) + 0.45 * jet, 0, 1)
""")

code(r"""
best_model = MODELS[BEST]
lconv = last_conv_layer_name(best_model)
print('Grad-CAM last conv layer:', lconv)

# Collect a few test images: correct high-conf, correct low-conf, misclassified
test_imgs = np.concatenate([x.numpy() for x, _ in test_ds_raw], axis=0)
probs_best = EVAL[BEST]['probs']; pred_best = EVAL[BEST]['y_pred']; conf = probs_best.max(1)
correct = pred_best == y_true
idx_hi  = np.where(correct & (conf > 0.9))[0][:3]
idx_lo  = np.where(correct & (conf < 0.6))[0][:2]
idx_wr  = np.where(~correct)[0][:3]
sel = list(idx_hi) + list(idx_lo) + list(idx_wr)
tags = ['correct hi'] * len(idx_hi) + ['correct lo'] * len(idx_lo) + ['WRONG'] * len(idx_wr)

plt.figure(figsize=(14, 6))
for k, (i, tag) in enumerate(zip(sel, tags)):
    img = test_imgs[i].astype('uint8')
    heat = make_gradcam_heatmap(test_imgs[i:i + 1], best_model, lconv, pred_index=int(pred_best[i]))
    plt.subplot(2, len(sel), k + 1); plt.imshow(img); plt.axis('off')
    plt.title('%s\nT:%s' % (tag, class_names[y_true[i]]), fontsize=7)
    plt.subplot(2, len(sel), len(sel) + k + 1); plt.imshow(overlay(img, heat)); plt.axis('off')
    plt.title('P:%s (%.2f)' % (class_names[pred_best[i]], conf[i]), fontsize=7)
plt.suptitle('Grad-CAM — %s (top row: input, bottom: heatmap)' % BEST)
plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'gradcam.png'), dpi=150); plt.show()
""")

# ---------------------------------------------------------------- 8. SHAP
md(r"""
## 7. Explainability — SHAP

SHAP attributes the prediction to individual image regions (positive = supports the class,
negative = opposes). We use `GradientExplainer` with a small background set and explain the top
predicted class. If SHAP fails on the runtime, an occlusion-sensitivity fallback is produced so the
figure always exists.
""")

code(r"""
SHAP_OK = False
try:
    import shap
    background = test_imgs[np.random.choice(len(test_imgs), 25, replace=False)].astype('float32')
    samples = test_imgs[sel[:3]].astype('float32')
    explainer = shap.GradientExplainer(best_model, background)
    shap_values, idx = explainer.shap_values(samples, ranked_outputs=1, nsamples=50)
    shap.image_plot(shap_values, samples / 255.0, show=False)
    plt.savefig(os.path.join(FIG_DIR, 'shap.png'), dpi=150, bbox_inches='tight'); plt.show()
    SHAP_OK = True
    print('SHAP figure saved.')
except Exception as ex:
    print('SHAP GradientExplainer failed (%s) -> occlusion-sensitivity fallback.' % type(ex).__name__)
""")

code(r"""
# Occlusion-sensitivity fallback (only runs if SHAP failed) — slides a grey patch and measures
# the drop in the predicted-class probability, an attribution map that always works.
if not SHAP_OK:
    def occlusion_map(img, model, cls, patch=32, stride=24):
        base = float(model(img[None].astype('float32'), training=False)[0, cls])
        H = (IMG_SIZE - patch) // stride + 1
        m = np.zeros((H, H))
        for a, r in enumerate(range(0, IMG_SIZE - patch + 1, stride)):
            for b, c in enumerate(range(0, IMG_SIZE - patch + 1, stride)):
                o = img.copy(); o[r:r + patch, c:c + patch] = 127
                m[a, b] = base - float(model(o[None].astype('float32'), training=False)[0, cls])
        return np.clip(m, 0, None)
    plt.figure(figsize=(12, 4))
    for k, i in enumerate(sel[:3]):
        img = test_imgs[i].astype('uint8')
        m = occlusion_map(test_imgs[i], best_model, int(pred_best[i]))
        plt.subplot(2, 3, k + 1); plt.imshow(img); plt.axis('off'); plt.title('input', fontsize=8)
        plt.subplot(2, 3, 3 + k + 1); plt.imshow(overlay(img, m / (m.max() + 1e-8))); plt.axis('off')
        plt.title('occlusion attribution', fontsize=8)
    plt.suptitle('Occlusion sensitivity (SHAP fallback) — %s' % BEST)
    plt.tight_layout(); plt.savefig(os.path.join(FIG_DIR, 'shap.png'), dpi=150); plt.show()
""")

# ---------------------------------------------------------------- 9. Save
md("## 8. Save models, results.json, and zip outputs")

code(r"""
# Save the best model for the web app
best_model.save(os.path.join(MODEL_DIR, 'best_model.keras'))
with open(os.path.join(OUT_DIR, 'class_names.json'), 'w') as f:
    json.dump(class_names, f)

results = {
    'project': 'Explainable Sports Category Classification',
    'dataset': DATASET_STATS,
    'class_names_count': NUM_CLASSES,
    'best_model': BEST,
    'models': {n: {k: v for k, v in e.items() if k not in ('probs', 'y_pred')} for n, e in EVAL.items()},
    'per_class_best5': BEST5,
    'per_class_worst5': WORST5,
    'top_confusions': TOP_CONFUSED,
    'shap_method': 'GradientExplainer' if SHAP_OK else 'occlusion-sensitivity-fallback',
    'config': dict(img_size=IMG_SIZE, batch_size=BATCH_SIZE, seed=SEED,
                   epochs_custom=EPOCHS_CUSTOM, epochs_head=EPOCHS_HEAD, epochs_finetune=EPOCHS_FINETUNE,
                   tf_version=tf.__version__),
    'rq_summary': {
        'RQ1_best_model': BEST,
        'RQ2_transfer_vs_custom': {
            'custom_f1': EVAL['Custom_CNN']['macro_f1'],
            'best_transfer_f1': max(EVAL[m]['macro_f1'] for m in EVAL if m != 'Custom_CNN')},
        'RQ4_efficiency': {n: {'macro_f1': EVAL[n]['macro_f1'], 'inference_ms': EVAL[n]['inference_ms'],
                               'model_size_mb': EVAL[n]['model_size_mb']} for n in EVAL},
    },
}
with open(os.path.join(OUT_DIR, 'results.json'), 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results['models'], indent=2)[:1500])
""")

code(r"""
# Bundle everything for the report
zip_path = os.path.join(OUT_DIR, 'results.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(OUT_DIR, 'results.json'), 'results.json')
    z.write(os.path.join(OUT_DIR, 'class_names.json'), 'class_names.json')
    for f in glob.glob(os.path.join(FIG_DIR, '*.png')):
        z.write(f, os.path.join('figures', os.path.basename(f)))
print('Wrote', zip_path)
print('Download results.zip + models/best_model.keras from the Output panel.')
""")

# ================================================================ serialize
def make_cell(kind, src):
    base = {"metadata": {}, "source": src}
    if kind == "md":
        base["cell_type"] = "markdown"
    else:
        base.update({"cell_type": "code", "outputs": [], "execution_count": None})
    return base


nb = {
    "cells": [make_cell(k, s) for k, s in cells],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
        "accelerator": "GPU",
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sports_cnn_explainable.ipynb")
with open(out, "w") as f:
    json.dump(nb, f, indent=1)
print("Wrote", out, "with", len(cells), "cells")
