# IRVE

The goal of this project is to analyse open data of infrastructure of electric vehciles and identify trends and insights

# Build
1. Download as md
2. pandoc rapport.md -s -o irve.docx # to export to word
3. jupyter nbconvert --to html --no-input rapport.ipynb --output index --HTMLExporter.theme=dark
