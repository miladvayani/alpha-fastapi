.. Fastapi Core Plugins documentation master file, created by
   sphinx-quickstart on Wed Mar  9 13:00:56 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Fastapi Core Plugins's documentation!
================================================

`Fast api core source codes <https://gitlab.hasebgostar.com/fastapi-core-plugs>`_

Sphinx help
============

.. important::

   Read the document below for use sphinx auto doc generator config settings

1. Go in ``docs`` directory and add **sphinx-quickstart** command to generate basics of documentation.

2. Set the following in your existing Sphinx documentation's ``conf.py`` file:

   .. code-block:: python

      sys.path.insert(0, os.path.abspath(".."))

   .. code-block:: python

      extensions = ["sphinx.ext.autodoc", "maisie_sphinx_theme"]

   .. code-block:: python

      import maisie_sphinx_theme

      html_theme = 'maisie_sphinx_theme'
      html_theme_path = maisie_sphinx_theme.html_theme_path()

   .. code-block:: python

      gettext_additional_targets = ["literal-block"]

3. Build your Sphinx documentation of all plugins automatically with command **sphinx-apidoc -o . ..**:

4. Then use **make html** command for generate new html file from your generated documents

Content
=======

   Html path: ``'_build/html/index.html'``

.. toctree::
   :maxdepth: 2

   modules