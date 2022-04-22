# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "Pyll JSON Errors"
copyright = "2020, LeafLink Engineering"
author = "LeafLink Engineering"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".gitkeep"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_js_files = ["pyll.js"]

html_theme_options = {
    "github_button": False,
    "github_user": "Leaflink",
    "github_repo": "pyll-json-errors",
    "show_powered_by": False,
    "extra_nav_links": {"GitHub Repo": "https://github.com/LeafLink/pyll-json-errors"},
    "body_text": "#1E164B",
    "link": "#9AD7D0",
    "link_hover": "#3CDBC0",
}
html_sidebars = {"**": ["logo.html", "navigation.html", "relations.html", "searchbox.html", "versions.html"]}

html_context = {
    "github_repo": "LeafLink/pyll-json-errors",
    "docs_host": "https://pyll-dev-docs.leaflink.com",
}

# -- InterSphinx Configuration ------------------------------------------------

intersphinx_mapping = {
    "flask": ("https://flask.palletsprojects.com/en/1.1.x", None),
    "marshmallow": ("https://marshmallow.readthedocs.io/en/stable/", None),
    "werkzeug": ("https://werkzeug.palletsprojects.com/en/1.0.x", None),
}

# -- External Links Configuration ---------------------------------------------

extlinks = {
    "drf_gh": ("https://github.com/encode/django-rest-framework/tree/master/%s", ""),
    "drf_ref": ("https://www.django-rest-framework.org/api-guide/%s", ""),
    "gh": ("https://github.com/LeafLink/pyll-json-errors/tree/master/%s", ""),
}
