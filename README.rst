Tutorial on writing scikit-learn compliant code
===============================================

.. image:: https://github.com/yngvem/sklearn-compliant/blob/master/LICENSE
    :target: https://github.com/yngvem/sklearn-compliant/blob/master/LICENSE

This tutorial will teach you to manage a project, publish it on PyPI and
create a scikit-learn compliant estimator. The project structure part of
this guide is majorly influenced by the following `tutorial
<https://blog.ionelmc.ro/2014/05/25/python-packaging/>_`.

Table of contents
-----------------

.. contents::


Structuring a repository
------------------------
An integral part of having reusable code is having a sensible repository
structure. That is, which files do we have and how do we organise them.
Unfortunately, figuring out how to structure a Python project best is not
a trivial task. In this part of the tutorial, I hope to show you a way
to initate any Python project to ensure that you won't have to do major
effort restructuring the code once you want to publish it.  

Let us start with the folder layout. Your project directory should
be structured in the following way and we will explain why later.

.. code::raw
   
   project_name
   ├── docs
   │   ├── make.bat
   │   ├── Makefile
   │   └── source
   │       ├── conf.py
   │       └── index.rst
   ├── examples
   │   └── example.py
   ├── src
   │   └── package_name
   │       └── __init__.py
   ├── tests
   │   └── __init__.py
   ├── LICENSE.txt
   ├── MANIFEST.in
   ├── README.rst
   ├── requirements.txt
   ├── setup.cfg
   ├── setup.py
   └── tox.ini

Now, this is a lot of files, let us look at these to understand what the
different components are and why they are necessary in a Python project.

**The ``setup`` files**  
The ``setup.py``, ``setup.cfg`` and ``MANIFEST.in`` files are used to
specify how a package should be installed. You might think that you don't
want to create an installable package, so let's skip this. DON'T! Even for
small projects, you should include these because of something called
editable installs (more on that later). The most basic setup.py file should
look like this

.. code::python

   from setuptools import setup

   setup()

Some projects might include more code, especially if you are using Cython
or creating C-extensions to Python. However, if you are not, then this style
will probably suffice. The reason we keep the ``setup.py`` minimal is that
we want to keep as much of the setup configuration as possible inside the
``setup.cfg`` file. This is to let other people parse metadata about our
package without running a Python file first! The ``setup.cfg`` file should
look like this

.. code::ini

   [metadata]      
   name = <package-name>
   version = <version number: 0.0.0>
   license = <lisence name, e.g. MIT>    
   description = <A short description>
   long_description = file: README.rst
   author = <Author name>
   author_email = <Optional: author e-mail>
   classifiers=
      <classifier 1>
      <classifier 2>
      <...>
      <classifier m>
            
   [options]
   packages = find:
   package_dir = 
       =src
   include_package_data = True
   install_requires = 
      <requirement 1>
      <requirement 2>
      <...>
      <requirement n>

   [options.packages.find]
   where=src

This file is formated using the ``ini`` standard, which you can read
more about with a quick search on DuckDuckGo. However, if you you
simply follow this layout, replacing the elements wrapped in ``<>`` with
the correct information for your package, then you are ok.

There are two sections here that might be confusing, the ``classifiers``
section and the ``install_requires`` section. The ``classifiers`` section is
used by PyPI to make it easier for new users to find your package, you can find a full list of classifiers `here<https://pypi.org/classifiers/>_`. Likewise, the
``install_requires`` section specifies which Python packages that ``pip`` should
install before installing the package you are developing. Both these fields are
optional, so you can leave them blank until you have anything to fill in.

Lastly, the ``MANIFEST.in`` file. This file is used to instruct setupttools
on which files it should include when it creates an installable project. For
a general project, I reccomend having a file with the following layout.

.. code::raw

   include setup.py
   include MANIFEST.in
   include LICENSE
   include README.md

   graft test
   graft examples
   graft docs
   graft src

**The ``requirements.txt`` file**  
The ``requirements.txt`` file is similar to the ``install_requires`` field in
the ``setup.cfg`` file we described above. However, the aim of the
``requirements.txt`` file is not to specify the dependencies of your package,
but the packages needed to work on developing your package. Each dependency
should be on a separate line. Here is an example of a ``requirements.txt``
file.

.. code::raw

   scikit-learn
   tox
   black
   isort
   -e .

We will depend on ``scikit-learn`` if we are to create scikit-learn compliant
code. Similarly, we need ``tox`` to run our test-suite. ``black`` and ``isort``
are two really good code auto-formatters, which you can read more about on
their GitHub pages (`black<https://github.com/psf/black>_` and `isort
<https://github.com/timothycrosley/isort>_`). Finally, with the ``-e .`` line
we install the current directory in editable mode.

Writing scikit-learn compliant code
-----------------------------------
Abbreviated version of the developer guide

Using continuous integration
----------------------------
Travis CI

Automatic coverage reporting
----------------------------
Coverall

Uploading to Pypi
-----------------

Automatic documentation
-----------------------
Readthedocs

