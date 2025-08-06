"""
PathFinder-AI / utils/nltk_setup.py
One-shot NLTK downloader for the virtual environment.
"""

import os
import nltk

PACKAGES = ["stopwords", "punkt", "wordnet"]

def main():
    venv = os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")
    if not venv:
        print("⚠️  Activate your virtual environment first.")
        return

    target = os.path.join(venv, "nltk_data")
    nltk.download(PACKAGES, download_dir=target, quiet=False)
    print("✅ NLTK resources ready at", target)

if __name__ == "__main__":
    main()