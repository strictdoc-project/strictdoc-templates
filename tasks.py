# Invoke is broken on Python 3.11
# https://github.com/pyinvoke/invoke/issues/833#issuecomment-1293148106
import inspect
import os
import re
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
def clean_itest_artifacts(context):
    # https://unix.stackexchange.com/a/689930/77389
    find_command = """
        git clean -dfX tests/integration/
    """
    # The command sometimes exits with 1 even if the files are deleted.
    # warn=True ensures that the execution continues.
    run_invoke(context, find_command, warn=True)


@task
def server(context, input_path="."):
    assert os.path.isdir(input_path), input_path
    run_invoke_with_tox(
        context,
        ToxEnvironment.CHECK,
        f"""
            strictdoc server {input_path} --reload
        """,
    )


@task
def test_integration(
    context,
    focus=None,
    debug=False,
    strictdoc=None,
    environment=ToxEnvironment.CHECK,
):
    clean_itest_artifacts(context)

    cwd = os.getcwd()

    if strictdoc is None:
        strictdoc_exec = f'strictdoc'
    else:
        strictdoc_exec = strictdoc

    focus_or_none = f"--filter {focus}" if focus else ""
    debug_opts = "-vv --show-all" if debug else ""

    itest_command = f"""
        lit
        --param STRICTDOC_EXEC="{strictdoc_exec}"
        -v
        {debug_opts}
        {focus_or_none}
        {cwd}/tests/integration
    """

    # It looks like LIT does not open the RUN: subprocesses in the same
    # environment from which it itself is run from. This issue has been known by
    # us for a couple of years by now. Not using Tox on Windows for the time
    # being.
    if os.name == "nt":
        run_invoke(context, itest_command)
        return

    run_invoke_with_tox(
        context,
        environment,
        itest_command,
    )


@task
def test(context):
    test_integration(context)


@task
def check(context):
    test(context)


@task
def check_dead_links(context):
    pass
    # run_invoke_with_tox(
    #     context,
    #     ToxEnvironment.CHECK,
    #     """
    #         python3 tools/link_health.py docs/strictdoc_01_user_guide.sdoc
    #     """,
    # )


@task
def watch(context, sdocs_path="."):
    strictdoc_command = f"""
        strictdoc
            export
            {sdocs_path}
            --output-dir output/
            --experimental-enable-file-traceability
    """

    run_invoke_with_tox(
        context,
        ToxEnvironment.CHECK,
        f"""
            {strictdoc_command}
        """,
    )

    paths_to_watch = "."
    run_invoke_with_tox(
        context,
        ToxEnvironment.CHECK,
        f"""
            watchmedo shell-command
            --patterns="*.py;*.sdoc;*.jinja;*.html;*.css;*.js"
            --recursive
            --ignore-pattern='output/;tests/integration'
            --command='{strictdoc_command}'
            --drop
            {paths_to_watch}
        """,
    )


@task
def run(context, command):
    run_invoke_with_tox(
        context,
        ToxEnvironment.CHECK,
        f"""
            {command}
        """,
    )
