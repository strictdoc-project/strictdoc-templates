# Invoke is broken on Python 3.11
# https://github.com/pyinvoke/invoke/issues/833#issuecomment-1293148106
import inspect
import os
import re
import shutil
import sys
from enum import Enum
from typing import Optional

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import invoke  # pylint: disable=wrong-import-position
from invoke import task  # pylint: disable=wrong-import-position

# Specifying encoding because Windows crashes otherwise when running Invoke
# tasks below:
# UnicodeEncodeError: 'charmap' codec can't encode character '\ufffd'
# in position 16: character maps to <undefined>
# People say, it might also be possible to export PYTHONIOENCODING=utf8 but this
# seems to work.
# FIXME: If you are a Windows user and expert, please advise on how to do this
# properly.
sys.stdout = open(  # pylint: disable=consider-using-with
    1, "w", encoding="utf-8", closefd=False, buffering=1
)


# To prevent all tasks from building to the same virtual environment.
# All values correspond to the configuration in the tox.ini config file.
class ToxEnvironment(str, Enum):
    CHECK = "check"


def run_invoke(
    context,
    cmd,
    environment: Optional[dict] = None,
    warn: bool = False,
) -> invoke.runners.Result:
    def one_line_command(string):
        return re.sub("\\s+", " ", string).strip()

    return context.run(
        one_line_command(cmd),
        env=environment,
        hide=False,
        warn=warn,
        pty=False,
        echo=True,
    )


def run_invoke_with_tox(
    context,
    environment_type: ToxEnvironment,
    command: str,
) -> invoke.runners.Result:
    assert isinstance(environment_type, ToxEnvironment)
    assert isinstance(command, str)
    tox_py_version = f"py{sys.version_info.major}{sys.version_info.minor}"
    return run_invoke(
        context,
        f"""
            tox
                -e {tox_py_version}-{environment_type.value} --
                {command}
        """,
    )


@task
def clean(context):
    # https://unix.stackexchange.com/a/689930/77389
    clean_command = """
        rm -rfv output/ docs/sphinx/build/
    """
    run_invoke(context, clean_command)


@task
def bitfield(context, input, output, lanes, bits):
    command = f"""bit_field --lanes {lanes} --bits {bits}   --fontsize 8  --hspace 750 --vspace 40 {input} > {output}"""
    run_invoke(context, command)


@task
def cairosvg(context, input, output):
    command = f"""cairosvg {input} -o {output}"""
    run_invoke(context, command)


@task
def readthedoc(context):
    strictdoc2rst(context, "templates/DO-178C/doc", "templates/DO-178C")
    doxygen(context, "templates/DO-178C/.doxygen")
    bitfield(
        context,
        "templates/DO-178C/_assets/A429.json",
        "templates/DO-178C/_assets/A429.svg",
        1,
        32,
    )
    cairosvg(
        context,
        "templates/DO-178C/_assets/A429.svg",
        "templates/DO-178C/_assets/A429.pdf",
    )


@task
def strictdoc2rst(context, input, output):
    command = f"""
        strictdoc export
            --output-dir {output}
            --project-title DO-178C
            --format rst {input}
    """
    run_invoke(context, command)


@task
def doxygen(context, config):
    command = f"""doxygen {config}"""
    run_invoke(context, command)


@task
def build_sphinx_html(context, input_path):
    path_to_build_sphinx_html = os.path.join(os.getcwd(), "build/sphinx_html")
    command = f"""
        cd {input_path} &&
        sphinx-build -W -b singlehtml . {path_to_build_sphinx_html}
    """
    run_invoke(context, command)


@task
def build_sphinx_html_programmatic(context):
    command = f"""
        python program.py
    """
    run_invoke(context, command)


@task
def build_html(context):
    # strictdoc2rst(context, "doc/", "build/strictdoc-rst/")
    os.makedirs("build/strictdoc-rst/", exist_ok=True)
    doxygen(context, ".doxygen")
    bitfield(
        context,
        "_assets/A429.json",
        "_assets/A429.svg",
        1,
        32,
    )
    cairosvg(
        context,
        "_assets/A429.svg",
        "_assets/A429.pdf",
    )
    path_to_rst_assets = "build/strictdoc-rst/rst/_assets"
    if os.path.exists(path_to_rst_assets):
        shutil.rmtree(path_to_rst_assets)
    shutil.copytree("_assets", path_to_rst_assets)

    shutil.copyfile("sphinx/index.rst", "build/strictdoc-rst/rst/index.rst")
    shutil.copyfile("sphinx/conf.py", "build/strictdoc-rst/rst/conf.py")
    shutil.copytree("sphinx/themes", "build/strictdoc-rst/rst/themes")

    # build_sphinx_html(context, input_path="build/strictdoc-rst/rst")
    build_sphinx_html_programmatic(context)
