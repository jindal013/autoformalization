#!/usr/bin/env python3

import subprocess
import sys


def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False


def main():
    print("Installing missing dependencies for Autoformalization...")

    packages = [
        "rank-bm25",
        "scikit-learn",
        "torch",
        "transformers",
        "langchain",
        "langchain-community",
        "faiss-cpu",
        "sentence-transformers",
        "numpy",
        "huggingface-hub",
    ]

    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1

    print(
        f"\nInstallation complete: {success_count}/{len(packages)} packages installed successfully"
    )

    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        print("\nYou can now run:")
        print(
            "  python formalize.py --query 'your mathematical statement' --method hybrid"
        )
        print(
            "  python simple_formalize.py --query 'your mathematical statement' --method keyword"
        )
    else:
        print(
            "⚠ Some packages failed to install. Please check the error messages above."
        )


if __name__ == "__main__":
    main()
