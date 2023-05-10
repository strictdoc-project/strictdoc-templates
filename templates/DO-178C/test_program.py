import shutil

from breathe import setup
from sphinx.application import Sphinx
import os


def rst_to_html():
    srcdir = os.path.join(os.getcwd(), "build/strictdoc-rst/rst")
    outdir = os.path.join(os.getcwd(), "build/wip_sphinx_html")
    doctreedir = os.path.join(srcdir, "doctrees")

    if os.path.exists(doctreedir):
        shutil.rmtree(doctreedir)
    if os.path.exists(doctreedir):
        shutil.rmtree(outdir)

    # Initialize and build the Sphinx application
    app = Sphinx(
        srcdir=srcdir,
        confdir=None,
        outdir=outdir,
        doctreedir=doctreedir,
        buildername="singlehtml"
    )
    setup(app=app)
    app.config["breathe_projects"] = {"DO-178C": "_xml"}
    app.build(force_all=True)


rst_to_html()
