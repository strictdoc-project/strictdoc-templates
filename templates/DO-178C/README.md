# StrictDoc template for DO-178C standard

This DO-178C template provides an overview of the documents required as acceptable mean of compliance.

The aim of the project is also to demonstrate the use of strictdoc integrating:
- diagrams (asciiflow)
- images
- bitfields
- doxygen
- sphinx pdf and readthedoc publication

For this purpose, a toy example is used.

Requirements:
```
apt install ninja-build
pip install sphinx
pip install sphinx_rtd_theme
pip install bit-field
pip install cairosvg
apt install doxygen
pip install breathe
apt install latexmk
apt install texlive-latex-base
apt install texlive-fonts-recommended
apt install texlive-latex-extra
```

To rebuild spinx html and pdf:
ninja

known limitations:
- requirement shall have a title to get proper sphinx cross reference.
- autodoxygenfile not supported by strictdoc
- assets ``img.*`` not displayed by strictdoc
