import click

from pathlib import Path


# fmt: off
MAIN = """#!/usr/bin/env python3\n"""

EXAMPLE_SHELL_SCRIPT = '''import click

@click.command(context_settings={{"show_default": True}})
@click.argument("name", type=str, nargs=1)
@click.argument("input_paths", type=Path, nargs=-1)
@click.option("-p","--param", help="gimme parameter", default="bla")
@click.option("-vp","--verbose", help="be verbose", is_flag=True)
def df_concat(name, input_paths: list[Path], param="bla", verbose=False) -> None:
    print(name, input_paths, param, verbose)
'''

GITIGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*egg-info
build
"""

LICENSE = "You have no right to use this code. It's all mine. Get out of here."

README = """# {module_name}

A short description of the project.
"""

MAKEFILE = """make:
    echo "Welcome to Project '{module_name}'"
upload_test_pypi:
    rm -rf dist || True
    python setup.py sdist
    twine -r testpypi dist/* 
upload_pypi:
    rm -rf dist || True
    python setup.py sdist
    twine upload dist/* 
"""

MANIFEST = """include README.md
include LICENSE
"""

PYPROJECT = """[build-system]
requires = ["setuptools >= 64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name="{module_name}"
version="0.0.1"
description="SHORT DESC."
readme="README.md"
authors=[
    {{name="{dev_name}",email="{dev_email}"}},
]
dependencies = [
    "click",
]
requires-python = ">=3.6"


[project.scripts]
example_shell_script = "{module_name}.cli.example_shell_script:example_shell_script"

[project.urls]
homepage="https://github.com/{dev_git_server_name}/{module_name}.git"
repository="https://github.com/{dev_git_server_name}/{module_name}.git"

[tool.uv]
reinstall-package = ["{module_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
"""

PYTEST_STANDARD = """[pytest]
python_files = {module_name}/*.py
"""

PYTEST_SRC = """[pytest]
python_files = src/{module_name}/*.py
"""
# fmt: on

file_structures: dict[str, dict[str, str]] = dict(
    standard={
        "{output}/tests/.keep": "",
        "{output}/{module_name}/__init__.py": "",
        "{output}/{module_name}/main.py": MAIN,
        "{output}/{module_name}/cli/example_shell_script.py": EXAMPLE_SHELL_SCRIPT,
        "{output}/.gitignore": GITIGNORE,
        "{output}/__init__.py": "",
        "{output}/LICENSE": LICENSE,
        "{output}/MAKEFILE": MAKEFILE,
        "{output}/MANIFEST.IN": MANIFEST,
        "{output}/pyproject.toml": PYPROJECT,
        "{output}/README.md": README,
        "{output}/pytest.ini": PYTEST_STANDARD,
    },
    src={
        "{output}/src/{module_name}/__init__.py": "",
        "{output}/src/{module_name}/main.py": MAIN,
        "{output}/src/{module_name}/cli/__init__.py": "",
        "{output}/src/{module_name}/cli/example_shell_script.py": EXAMPLE_SHELL_SCRIPT,
        "{output}/.gitignore": GITIGNORE,
        "{output}/__init__.py": "",
        "{output}/LICENSE": LICENSE,
        "{output}/MAKEFILE": MAKEFILE,
        "{output}/MANIFEST.IN": MANIFEST,
        "{output}/pyproject.toml": PYPROJECT,
        "{output}/README.md": README,
        "{output}/pytest.ini": PYTEST_SRC,
    },
)


@click.command(context_settings={"show_default": True})
@click.argument("output", type=Path)
@click.option("--dev_name", default="MatteoLacki", help="Name of the developer.")
@click.option("--dev_email", default="matteo.lacki@gmail.com", help="Dev's Email")
@click.option(
    "--exist_ok",
    help="Make it OK to write to an existing folder.",
    is_flag=True,
)
@click.option(
    "--file_structure",
    type=click.Choice(file_structures, case_sensitive=False),
    help="Choose a file structure.",
    default="standard",
    show_default=True,
)
def create_python_module(
    output,
    dev_name: str,
    dev_email: str,
    exist_ok: bool = False,
    file_structure: str = "standard",
) -> None:
    module_name = output.name
    dev_git_server_name = dev_name

    fs = file_structures[file_structure]

    output.mkdir(parents=True, exist_ok=exist_ok)
    for path, content in fs.items():
        path = Path(path.format(**locals()))
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as file:
            file.write(content.format(**locals()))
