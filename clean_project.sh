find . -name "*.pyc" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;
find . -name ".DS_Store" -exec rm -f {} \;
rm -rf myenv/