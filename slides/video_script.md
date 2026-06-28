# Presentation video — spoken script (~10 minutes = ~2 min live demo + ~8 min slides)

Read naturally. Start with the **live demo** of the deployed web app, then go through the slides
(one block per slide). Replace [bracketed] numbers with your real results after the Kaggle run.
Target: under 10 minutes total (the professor's cap).

---

## Part 1 — Live demo of the web interface (~2 min)

[Open the deployed Hugging Face Space in the browser beforehand so it is already loaded.]
"Before the slides, here is the working system. This is my Explainable Sports Classifier, running
live on Hugging Face Spaces. I'll upload a sports image — [drag in a test image, e.g. a Formula 1
photo]. Within about a second it returns the top-5 predicted sports with confidence scores — here the
top prediction is [formula 1 racing] at [9X]% confidence. On the right is the Grad-CAM heatmap: the
warm region sits on [the car and the track], which shows the model is looking at sport-relevant
content, not the background. Let me try a harder example — [upload a second image] — and you can see
the top-5 and the heatmap update. This is the same model and the same preprocessing I evaluate in the
report, so what you see live is exactly what the reported numbers measure. Now to the slides for how
it was built and what the results show."

---

## Part 2 — Slides (~8 min)

**[Slide 1 — Title]**
"Hi, I'm Arda Tekin Tezel. This is my Machine Learning and Smart Systems project on *Explainable
Sports Category Classification using CNN transfer learning*. I compare a custom CNN with two
pretrained networks — EfficientNetV2 and ConvNeXt-Tiny — and I explain the best model's decisions
using Grad-CAM and SHAP."

**[Slide 2 — Problem]**
"Sports media platforms and archives hold millions of images that need to be tagged by sport for
search, indexing, and analytics. Doing this by hand is slow, expensive, and inconsistent. So the
goal is an automatic classifier that recognizes the sport in an image across 100 categories — and,
crucially, one whose reasoning we can inspect and trust."

**[Slide 3 — Dataset]**
"I use the public 100 Sports Image Classification dataset from Kaggle. It has 100 sports classes and
about 14,500 images, already split into 13,493 training, 500 validation, and 500 test images, all at
224 by 224 pixels. Here are sample images and the class distribution — the dataset is fairly
balanced across classes."

**[Slide 4 — Research questions]**
"I ask five questions: which model classifies sports best; whether transfer learning beats a custom
CNN; whether the explanations focus on the athletes and equipment rather than the background; which
model gives the best trade-off between accuracy, speed, and size; and whether the best model can be
deployed as a working web demo."

**[Slide 5 — Methodology]**
"The pipeline is: load and inspect the data, preprocess to 224 by 224, apply augmentation — a
horizontal flip, small rotation, zoom, and contrast — then train three models, evaluate them, run
Grad-CAM and SHAP, and finally deploy the best one. Everything is seeded for reproducibility."

**[Slide 6 — Models]**
"The baseline is a custom CNN with four convolutional blocks. The two transfer-learning models start
from ImageNet weights; I first train a new classification head with the backbone frozen, then
fine-tune the top thirty percent of the backbone at a low learning rate."

**[Slide 7 — Training]**
"These are the training and validation curves. All models converge, early stopping restores the best
weights, and the gap between training and validation accuracy shows the augmentation kept overfitting
under control."

**[Slide 8 — Results]**
"On the test set, the best model is [EfficientNetV2-B0] with about [91]% accuracy and [89.5]% macro-F1,
compared with about [81]% for the custom CNN. So transfer learning clearly helps — that answers RQ1
and RQ2. The transfer models are also smaller-error and faster per image."

**[Slide 9 — Class-level]**
"The confusion matrix shows most errors happen between visually similar sports — for example
[bowling and bocce, or different racquet sports]. The best-recognized classes have very distinctive
scenes, while the hardest ones share equipment or settings."

**[Slide 10 — Explainability]**
"Grad-CAM shows the model attends to the athlete, the ball, and the playing area rather than the
background, which supports RQ3. SHAP gives a complementary pixel-level attribution, and the two
methods agree on the important regions for correct predictions — and reveal background reliance on
some of the wrong ones."

**[Slide 11 — Efficiency & demo]**
"On the accuracy-versus-efficiency trade-off, [EfficientNetV2-B0] wins — best accuracy at the lowest
inference time. I deployed it as a Gradio web app: you upload an image and get the top-5 sports plus
a live Grad-CAM heatmap. That answers RQ4 and RQ5."

**[Slide 12 — Limitations & conclusion]**
"Limitations: a single public dataset, no external validation, and heatmaps are not proof of correct
reasoning. In conclusion, transfer learning with [EfficientNetV2-B0] gives an accurate, efficient,
and explainable sports classifier that runs in a browser. All code, the report, and the live demo
are linked here. Thank you."
