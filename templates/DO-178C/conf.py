# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DO-178C'
copyright = '2023, company'
author = 'John Doe'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['breathe','sphinx_rtd_theme']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
breathe_projects = {
    "DO-178C" : "rst/_xml" 
}
breathe_projects_source = {
    "DO-178C" : (
        "include",["imu.h"]
    )
}
# latex_logo='projectlogo.png'
latex_maketitle = r'''
\begin{titlepage}
\noindent \Huge DO-178C toy example
\sphinxlogo
\normalsize \par Written by : John Doe\newline 
Date: \today\newline
Approved by : \newline
\copyright 2023 Company
\end{titlepage}
'''

latex_elements = {     'classoptions': ',openany,oneside',
    'papersize':'a4paper',
    'maketitle': latex_maketitle}
breathe_default_project = 'DO-178C'
