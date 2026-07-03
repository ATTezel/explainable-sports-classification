# Video Transcript — word-for-word (~9.5 min, under the 10-minute cap)

**How to use:** read this out loud at a calm pace. Timings are guides. Structure =
~2 min live demo first, then ~7 min over the 12 slides, leaving ~0.5 min buffer.
Every number here matches the executed Kaggle run (`results.json`) and the report.

**Before you hit record:**
- Open the live app in your browser and upload one image once so it is "warm" (first load is slow).
  → https://huggingface.co/spaces/Tezo44/explainable-sports-classifier
- Have **two** test images ready on your desktop: one easy (e.g. basketball / Formula 1),
  one harder. Replace the [bracketed] cues with what you actually see on the day.
- Have the slide deck open full-screen in a second window.

---

## PART 1 — LIVE DEMO (~2:00)

"Hi, my name is Arda Tekin Tezel, and this is my Machine Learning and Smart Systems project:
an **Explainable Sports Category Classifier**. Before the slides, let me show you the finished
system actually running.

This is my web app, deployed live on Hugging Face Spaces — anyone can open this link in a browser.
I'll upload a sports image. [*drag in image 1*]. In about a second it returns the **top five** most
likely sports, each with a confidence score — here the top prediction is [*basketball*] at [*94*]
percent. On the right is the **Grad-CAM** heatmap: the warm region shows where the model looked to
make its decision. You can see it sits on [*the player and the ball*], not the crowd or the
background — which is exactly what we want: the model is using sport-relevant evidence.

Let me try one more — [*drag in image 2*]. Again, the top five predictions and a fresh heatmap.
This is the same trained model, with the same preprocessing, that I evaluate in my report — so what
you see live is exactly what my reported numbers measure. Now let me walk you through how I built it
and what I found."

---

## PART 2 — SLIDES (~7:00)

**[Slide 1 — Title] (~20s)**
"My project compares three convolutional neural networks for classifying images into one hundred
different sports, and then explains the best model's decisions using two methods — Grad-CAM and SHAP.
The three models are a custom CNN I built from scratch, and two pretrained networks: EfficientNetV2-B0
and ConvNeXt-Tiny."

**[Slide 2 — Problem & motivation] (~35s)**
"Why does this matter? Broadcasters, news outlets, and media archives store millions of images that
have to be tagged by sport so they can be searched and retrieved. Doing that by hand is slow,
expensive, and inconsistent. An automatic classifier solves that — but accuracy alone isn't enough.
If we're going to trust an automated tag, we need to know the model is looking at the athlete and the
equipment, not just guessing from the background. So my goal was a classifier that is both **accurate
and explainable**."

**[Slide 3 — Dataset] (~30s)**
"I used the public 100 Sports Image Classification dataset from Kaggle. It has one hundred sports
categories and about fourteen-and-a-half thousand images, already split by the authors into 13,493
training, 500 validation, and 500 test images — all at 224 by 224 pixels. As these charts show, the
dataset is fairly balanced, around 135 images per class, so no single sport dominates."

**[Slide 4 — Research questions] (~30s)**
"I organized the work around five research questions. One — which model classifies sports best?
Two — does transfer learning actually beat a custom CNN? Three — do the explanations focus on the right
regions, the athletes and equipment, rather than the background? Four — which model gives the best
trade-off between accuracy, speed, and size? And five — can the best model be deployed as a working
web demo?"

**[Slide 5 — Methodology pipeline] (~35s)**
"This is the pipeline. I load and inspect the data, preprocess every image to 224 by 224, and apply
light augmentation — a horizontal flip, a small rotation, zoom, and contrast change — which adds variety
without distorting the sport. Then I train all three models under identical conditions, evaluate them
with the same metrics, run Grad-CAM and SHAP, and deploy the best model. Everything uses a fixed random
seed, so the results are reproducible."

**[Slide 6 — Models] (~35s)**
"The baseline is my custom CNN — four convolutional blocks trained from scratch, with no outside
knowledge. The two transfer-learning models start from ImageNet-pretrained weights. For those I use a
two-stage strategy: first I freeze the backbone and train only a new classification head, then I
unfreeze the top thirty percent of the backbone and fine-tune it at a very low learning rate. That
preserves the general visual features while adapting the model to sports."

**[Slide 7 — Training behaviour] (~25s)**
"These are the training curves. All three models converged cleanly, and early stopping restored the
best weights. The narrow gap between the training and validation lines for the pretrained models shows
the augmentation kept overfitting under control — whereas the custom CNN, training from scratch, shows a
much wider gap."

**[Slide 8 — Results] (~45s)**
"Here are the headline results on the held-out test set. The best model is **ConvNeXt-Tiny**, at
**96.4 percent** accuracy and 96.3 percent macro-F1. EfficientNetV2-B0 is right behind it at 96.2
percent. And the custom CNN, trained from scratch, reaches only **47.2 percent**. So transfer learning
gives a roughly **forty-nine-point** jump in accuracy. That answers my first two research questions:
ConvNeXt-Tiny is the most accurate model, and transfer learning decisively beats the custom baseline.
The top-three and top-five accuracies for the pretrained models are above 99 percent, meaning the
correct sport is almost always among their top guesses."

**[Slide 9 — Class-level analysis] (~35s)**
"Looking deeper with the confusion matrix: most errors happen between sports that genuinely look alike
in a single frame. The two most common mistakes were horseshoe pitching confused with frisbee, and
baton twirling confused with javelin — both involve an athlete throwing or twirling a small object with
a similar posture. The best-recognized classes, like wingsuit flying and weightlifting, scored a
perfect F1 of one-point-zero. So the errors aren't random — they're concentrated on a small set of
fine-grained look-alikes."

**[Slide 10 — Explainability: Grad-CAM + SHAP] (~40s)**
"Now the explainability, which is the heart of the project. Grad-CAM produces these heatmaps, and for
correctly classified images they consistently land on the athlete, the equipment, and the playing area
— not the background. That's strong evidence the model reasons from sport-relevant content, which
answers research question three. SHAP gives a complementary, finer-grained pixel-level view, and for the
confident correct predictions the two methods agree on the same important regions. And on some of the
wrong predictions, the attention drifts to the background — which is exactly the kind of shortcut
behaviour the explainability is designed to expose."

**[Slide 11 — Efficiency & web demo] (~35s)**
"On efficiency — research question four — there's a real trade-off. ConvNeXt-Tiny is the most accurate,
but it's also the largest and slowest, at about 112 megabytes and 113 milliseconds per image.
EfficientNetV2-B0 matches its accuracy to within 0.2 points — a single test image — at about one-fifth
the size and one-twelfth the latency. So for a real-world deployment, EfficientNetV2-B0 is the smart
choice. And for research question five, I deployed the system as the live Gradio web app you saw at the
start."

**[Slide 12 — Limitations, conclusion & links] (~35s)**
"To be honest about the limitations: I used a single dataset with no external validation, the test set
is small at five images per class, and a heatmap shows where the model looks but isn't a formal proof of
correct reasoning. In conclusion: transfer learning produced an accurate and explainable sports
classifier — ConvNeXt-Tiny at 96.4 percent, with EfficientNetV2-B0 as the efficient alternative — and it
runs live in a browser with visual explanations. All my code, the full report, and the live demo are
linked here. Thank you for watching, and I'm happy to answer any questions."

---

### Quick number sheet (so you never misspeak)
| Model | Accuracy | Macro-F1 | Size | Latency |
|---|---|---|---|---|
| Custom CNN (from scratch) | 47.2% | 42.9% | 1.9 MB | 0.6 ms |
| EfficientNetV2-B0 (efficient pick) | 96.2% | 96.0% | 24 MB | 9.6 ms |
| **ConvNeXt-Tiny (best / deployed)** | **96.4%** | **96.3%** | 112 MB | 113 ms |

- Transfer-learning gap over custom CNN: **~49 accuracy points**.
- Top-3 / Top-5 (pretrained): **>99%**. Best classes F1 = 1.0 (wingsuit flying, weightlifting…).
- Top confusions: horseshoe pitching→frisbee, baton twirling→javelin.
- RQ1 ConvNeXt-Tiny · RQ2 transfer wins · RQ3 Grad-CAM/SHAP on sport regions · RQ4 EfficientNetV2-B0 · RQ5 live Gradio app.
