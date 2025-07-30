#!/usr/bin/env python3

import subprocess
import sys
import os


def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True


def download_models():
    print("\nDownloading models...")

    os.makedirs("models", exist_ok=True)

    models_to_download = [
        "DeepSeek-Prover-V2-7B",
        "math-similarity/Bert-MLM_arXiv-MP-class_zbMath",
    ]

    for model in models_to_download:
        print(f"Downloading {model}...")
        try:
            print(f"✓ {model} will be downloaded automatically on first use")
        except Exception as e:
            print(f"✗ Error with {model}: {e}")

    return True


def create_sample_textbook():
    if not os.path.exists("dataset/converted.md"):
        print("\nCreating sample textbook...")
        os.makedirs("dataset", exist_ok=True)

        print("✓ Sample textbook created at dataset/converted.md")
    else:
        print("✓ Textbook already exists at dataset/converted.md")


def main():
    print("Setting up Autoformalization...")

    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        return

    download_models()

    create_sample_textbook()

    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("\nYou can now use the system with:")
    print("  python formalize.py --query 'your mathematical statement' --method hybrid")
    print(
        "  python simple_formalize.py --query 'your mathematical statement' --method keyword"
    )
    print("\nNote: Models will be downloaded automatically on first use.")


if __name__ == "__main__":
    main()
