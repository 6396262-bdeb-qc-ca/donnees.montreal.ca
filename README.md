# Montreal_Donnees

![PyPI version](https://img.shields.io/pypi/v/donnees.montreal.ca.svg)

Le site des données ouvertes de la Ville de Montréal

* [GitHub](https://github.com/6396262-bdeb-qc-ca/donnees.montreal.ca/) | [PyPI](https://pypi.org/project/donnees.montreal.ca/) | [Documentation](https://6396262-bdeb-qc-ca.github.io/donnees.montreal.ca/)
* Created by [Alexander Campos](https://audrey.feldroy.com/) | GitHub [@6396262-bdeb-qc-ca](https://github.com/6396262-bdeb-qc-ca) | PyPI [@6396262-bdeb-qc-ca](https://pypi.org/user/6396262-bdeb-qc-ca/)
* MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://6396262-bdeb-qc-ca.github.io/donnees.montreal.ca/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/donnees.montreal.ca.git
cd donnees.montreal.ca

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `dm`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

Montreal_Donnees was created in 2026 by Alexander Campos.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
