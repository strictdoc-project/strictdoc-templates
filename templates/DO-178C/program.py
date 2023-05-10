import logging
import os
import shutil
import time
from typing import Iterator, Any

from breathe import setup
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import StringOutput
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.util import relative_uri
from sphinx.writers.html import HTMLWriter

# Force Sphinx to produce no logs.
logging.disable(logging.CRITICAL)


class StrictDocBuilder(SingleFileHTMLBuilder):
    name = 'strictdoc'
    format = 'custom'

    def __init__(self, app: Sphinx, env: BuildEnvironment = None) -> None:
        super().__init__(app, env)
        self.init()
        assert self.highlighter is not None
        # self.indexer = None
        self.output = None

    def prepare_writing(self, docnames):
        # self.docwriter = HTMLWriter(self)
        # self.docsettings: Any = OptionParser(
        #     defaults=self.env.settings,
        #     components=(self.docwriter,),
        #     read_config_files=True).get_default_values()

        super().prepare_writing(docnames)

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        # super().write_doc(docname, doctree)
        destination = StringOutput(encoding='utf-8')
        doctree.settings = self.docsettings

        self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        self.fignumbers = self.env.toc_fignumbers.get(docname, {})
        self.imgpath = relative_uri(self.get_target_uri(docname), '_images')
        self.dlpath = relative_uri(self.get_target_uri(docname), '_downloads')
        self.current_docname = docname

        self.docwriter.write(doctree, destination)
        self.docwriter.assemble_parts()
        body = self.docwriter.parts['fragment']
        metatags = self.docwriter.clean_meta
        # assert 0, body
        # self.output = body
        # ctx = self.get_doc_context(docname, body, metatags)
        # self.handle_page(docname, ctx, event_arg=doctree)

    def finish(self) -> None:
        # super().finish()
        pass


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
    # app.builder = app.create_builder("strictdoc")
    builder = StrictDocBuilder(app, app.env)
    builder.use_index = False

    app.registry.builders["custom"] = builder
    app.builder = app.registry.builders["custom"]
    app.config.breathe_projects = {"DO-178C": "_xml"}
    app.config.html_sidebars = {
        '**': [],
    }

    setup(app=app)

    start_time = time.perf_counter()

    for i in range(100):
        if os.path.exists(doctreedir):
            shutil.rmtree(doctreedir)
        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        app.build(
            force_all=False, filenames=["build/strictdoc-rst/rst/index.rst"],
        )

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")

rst_to_html()
