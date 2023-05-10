import logging
import os
import shutil
import time
from typing import Iterator, Any, Iterable, Optional, Sequence

from breathe import setup
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import StringOutput
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.util import relative_uri, status_iterator
from sphinx.util.parallel import SerialTasks
from sphinx.writers.html import HTMLWriter

# Force Sphinx to produce no logs.
logging.disable(logging.CRITICAL)


class StrictDocBuilder(SingleFileHTMLBuilder):
    name = 'strictdoc'
    format = 'custom'

    def __init__(self, app: Sphinx, env: BuildEnvironment = None) -> None:
        super().__init__(app, env)
        self.init()

        self.doctree = None
        self.indexer = None
        self.output = None
        self.strictdoc_output = None

    def build(
        self, docnames: Iterable[str], summary: Optional[str] = None, method: str = 'update'
    ) -> None:
        updated_docnames = set(self.read())

        doccount = len(updated_docnames)
        for docname in self.env.check_dependents(self.app, updated_docnames):
            updated_docnames.add(docname)
        outdated = len(updated_docnames) - doccount

        if updated_docnames:
            # global actions
            self.env.check_consistency()

        # filter "docnames" (list of outdated files) by the updated
        # found_docs of the environment; this will remove docs that
        # have since been removed
        if docnames and docnames != ['__all__']:
            docnames = set(docnames) & self.env.found_docs


        self.parallel_ok = False

        self.finish_tasks = SerialTasks()

        # write all "normal" documents (or everything for some builders)
        self.write(docnames, list(updated_docnames), method)

        # finish (write static files etc.)
        self.finish()

        # wait for all tasks
        self.finish_tasks.join()

    def write(self, build_docnames: Iterable[str], updated_docnames: Sequence[str], method: str = 'update') -> None:  # NOQA
        if build_docnames is None or build_docnames == ['__all__']:
            # build_all
            build_docnames = self.env.found_docs
        if method == 'update':
            # build updated ones as well
            docnames = set(build_docnames) | set(updated_docnames)
        else:
            docnames = set(build_docnames)

        # add all toctree-containing files that may have changed
        for docname in list(docnames):
            for tocdocname in self.env.files_to_rebuild.get(docname, set()):
                if tocdocname in self.env.found_docs:
                    docnames.add(tocdocname)
        docnames.add(self.config.root_doc)

        self.prepare_writing(docnames)

        for docname in docnames:
            assert self.doctree is not None
            doctree = self.doctree
            # self.write_doc_serialized(docname, doctree)
            self.write_doc(docname, doctree)

    def prepare_writing(self, docnames):
        self.docwriter = HTMLWriter(self)
        self.docsettings: Any = OptionParser(
            defaults=self.env.settings,
            components=(self.docwriter,),
            read_config_files=True).get_default_values()
        pass
        # super().prepare_writing(docnames)

    def write_doctree(self, docname: str, doctree: nodes.document) -> None:
        self.doctree = doctree

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        # super().write_doc(docname, doctree)
        destination = StringOutput(encoding='utf-8')
        doctree.settings = self.docsettings
        #
        # self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        # self.fignumbers = self.env.toc_fignumbers.get(docname, {})
        # self.imgpath = relative_uri(self.get_target_uri(docname), '_images')
        # self.dlpath = relative_uri(self.get_target_uri(docname), '_downloads')
        # self.current_docname = docname
        #
        self.docwriter.write(doctree, destination)
        self.docwriter.assemble_parts()
        body = self.docwriter.parts['fragment']
        self.strictdoc_output = body

        # metatags = self.docwriter.clean_meta
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

    if os.path.exists(doctreedir):
        shutil.rmtree(doctreedir)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)

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
