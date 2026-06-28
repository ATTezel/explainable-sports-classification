#!/usr/bin/env bash
# Push the notebook to Kaggle, run it on a free GPU, wait, and download the outputs
# (results.json, all figures, results.zip, best_model.keras, class_names.json).
#
# PREREQUISITE — a Kaggle API token at ~/.kaggle/kaggle.json:
#   1. kaggle.com -> your avatar -> Settings -> API -> "Create New Token"
#   2. mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
#
# Then, ONE edit: put your Kaggle username in notebook/kernel-metadata.json (replace KAGGLE_USERNAME).
#
# Usage:  cd notebook && bash run_on_kaggle.sh
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
  echo "ERROR: ~/.kaggle/kaggle.json not found. Create a Kaggle API token first (see header)." >&2
  exit 1
fi
command -v kaggle >/dev/null 2>&1 || { echo "Installing kaggle CLI..."; pip install --quiet kaggle; }

USER_ID=$(python3 -c "import json;print(json.load(open('$HOME/.kaggle/kaggle.json'))['username'])")
SLUG="$USER_ID/explainable-sports-cnn"
echo ">> Setting kernel id to $SLUG"
python3 - "$USER_ID" <<'PY'
import json,sys
u=sys.argv[1]
m=json.load(open("kernel-metadata.json"))
m["id"]=f"{u}/explainable-sports-cnn"
json.dump(m,open("kernel-metadata.json","w"),indent=2)
print("kernel-metadata.json updated")
PY

echo ">> Pushing kernel to Kaggle..."
kaggle kernels push -p .

echo ">> Waiting for the run to finish (GPU; this can take 30-90 min)..."
TRIES=0; MAX_TRIES=180   # hard cap: 180 x 60s = 3 hours, so a stuck kernel never hangs forever
while true; do
  sleep 60
  TRIES=$((TRIES + 1))
  if [ "$TRIES" -ge "$MAX_TRIES" ]; then
    echo ">> Timed out after $MAX_TRIES minutes. Check the kernel on kaggle.com." >&2; exit 3
  fi
  STATUS=$(kaggle kernels status "$SLUG" 2>/dev/null | tr -d '"' || true)
  echo "   [$TRIES/$MAX_TRIES] status: $STATUS"
  case "$STATUS" in
    *complete*) echo ">> Run complete."; break ;;
    *error*|*cancel*) echo ">> Run failed: $STATUS" >&2; exit 2 ;;
  esac
done

echo ">> Downloading outputs into ./kaggle_output ..."
mkdir -p kaggle_output
kaggle kernels output "$SLUG" -p kaggle_output
echo ">> Done. Files:"
ls -la kaggle_output
echo
echo "Next steps:"
echo "  1. Figures -> report:  (from repo root)  cd report && unzip -o ../notebook/kaggle_output/results.zip"
echo "     (the zip already contains a figures/ folder, so PNGs land at report/figures/*.png)."
echo "  2. Update the report numbers from kaggle_output/results.json (replace the red \\res{} placeholders)."
echo "  3. Copy best_model.keras + class_names.json into app/ for the Hugging Face Space."
