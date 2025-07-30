# run this script to convert the pdf (already done)

udo apt-get update
sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools
# conda create -n olmocr python=3.11
# conda activate olmocr
pip install olmocr
python -m olmocr.pipeline ./converted --markdown --pdfs ConciseRevised.pdf