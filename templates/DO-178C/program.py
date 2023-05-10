import logging
import os
import shutil
import time

from breathe import setup
from sphinx.application import Sphinx

# Force Sphinx to produce no logs.
logging.disable(logging.CRITICAL)

def rst_to_html():
    srcdir = os.path.join(os.getcwd(), "build/strictdoc-rst/rst")
    outdir = os.path.join(os.getcwd(), "build/wip_sphinx_html")
    doctreedir = os.path.join(srcdir, "build/strictdoc-rst/rst/doctrees")

    # if os.path.exists(doctreedir):
    #     shutil.rmtree(doctreedir)
    # if os.path.exists(outdir):
    #     shutil.rmtree(outdir)

    confoverrides = {}
    confoverrides["html_theme"] = "my_theme"
    confoverrides["html_theme_path"] = ["themes"]

    # Initialize and build the Sphinx application
    app = Sphinx(
        srcdir=srcdir,
        confdir=None,
        outdir=outdir,
        doctreedir=doctreedir,
        confoverrides=confoverrides,
        buildername="singlehtml"
    )

    app.config.breathe_projects = {"DO-178C": "_xml"}
    app.config.html_sidebars = {
        '**': [],
    }

    setup(app=app)

    start_time = time.perf_counter()

    for i in range(20):
        if os.path.exists(doctreedir):
            shutil.rmtree(doctreedir)
        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        app.build(
            force_all=False, # filenames=["build/strictdoc-rst/rst/test.rst"]
        )

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")

rst_to_html()
