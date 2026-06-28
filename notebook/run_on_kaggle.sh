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
while true; do
  sleep 60
  STATUS=$(kaggle kernels status "$SLUG" 2>/dev/null | tr -d '"' || true)
  echo "   status: $STATUS"
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
echo "Next: unzip kaggle_output/results.zip into report/figures/ and update the report numbers from results.json,"
echo "then move best_model.keras + class_names.json into app/ for the Hugging Face Space."
