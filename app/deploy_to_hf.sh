#!/usr/bin/env bash
# One-command deploy of this app/ folder to a (free) Hugging Face Space.
#
# Prereq: a Hugging Face account + a WRITE access token from
#         https://huggingface.co/settings/tokens
#
# Usage:
#   HF_USER=<your-hf-username> HF_TOKEN=hf_xxx bash deploy_to_hf.sh [space-name]
#
# It creates (or reuses) a Gradio Space and uploads app.py, requirements.txt,
# README.md, class_names.json, and best_model.keras (large file -> handled via LFS).
# When it finishes it prints the public URL — paste that into the report and the
# Teams submission as the "web link for the interface".
set -euo pipefail

SPACE="${1:-explainable-sports-classifier}"
: "${HF_USER:?Set HF_USER to your Hugging Face username}"
: "${HF_TOKEN:?Set HF_TOKEN to a write token from https://huggingface.co/settings/tokens}"

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

if [ ! -f best_model.keras ]; then
  echo "ERROR: best_model.keras is missing next to app.py."
  echo "Copy it from the Kaggle output: notebook/kaggle_output/models/best_model.keras"
  exit 1
fi

python3 -m pip install --quiet --upgrade "huggingface_hub>=0.25,<0.26"

HF_USER="$HF_USER" HF_TOKEN="$HF_TOKEN" SPACE="$SPACE" python3 - <<'PY'
import os
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])
repo_id = f'{os.environ["HF_USER"]}/{os.environ["SPACE"]}'
api.create_repo(repo_id, repo_type="space", space_sdk="gradio", exist_ok=True)
for f in ["README.md", "app.py", "requirements.txt", "class_names.json", "best_model.keras"]:
    print("uploading", f, "...", flush=True)
    api.upload_file(path_or_fileobj=f, path_in_repo=f, repo_id=repo_id, repo_type="space")
print("\nDONE -> https://huggingface.co/spaces/" + repo_id)
print("The Space will build for a few minutes (the 248 MB model takes a moment to load).")
PY
