Tutorial on managing a project
==============================

This tutorial will teach you to manage a project, and publish it on PyPI. 
This guide is majorly influenced by the following `tutorial
<https://blog.ionelmc.ro/2014/05/25/python-packaging/>`_.

Also, this tutorial will always be a work in progress (or at least so long
as best practice can change), so the tutorial might change at any time.
However, you can always read old versions of the tutorial,  since it is
covered by source control. Finally, if you have any constructive critic on the
contents in this tutorial, please raise an Issue with the Issue tracker.

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

.. code-block:: raw
   
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
   │   └── __init__.py
   ├── .gitignore
   ├── LICENSE.txt
   ├── MANIFEST.in
   ├── README.rst
   ├── requirements.txt
   ├── setup.cfg
   ├── setup.py
   └── tox.ini

Now, this is a lot of files, let us look at these to understand what the
different components are and why they are necessary in a Python project.

The ``setup`` files
^^^^^^^^^^^^^^^^^^^

The ``setup.py``, ``setup.cfg`` and ``MANIFEST.in`` files are used to
specify how a package should be installed. You might think that you don't
want to create an installable package, so let's skip this. DON'T! Even for
small projects, you should include these because of something called
editable installs (more on that later). The most basic setup.py file should
look like this

.. code-block:: python

   from setuptools import setup

   setup()

Some projects might include more code, especially if you are using Cython
or creating C-extensions to Python. However, if you are not, then this style
will probably suffice. The reason we keep the ``setup.py`` minimal is that
we want to keep as much of the setup configuration as possible inside the
``setup.cfg`` file. This is to let other people parse metadata about our
package without running a Python file first! The ``setup.cfg`` file should
look like this

.. code-block:: ini

   [metadata]      
   name = <package-name>
   version = <version number: 0.0.0>
   license = <license name, e.g. MIT>    
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

This file is formated according to `this
<https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files>`_
specification. However, if you you
simply follow the layout above, replacing the elements wrapped in ``<>`` with
the correct information for your package, then you are ok.

There are two sections here that might be confusing, the ``classifiers``
section and the ``install_requires`` section. The ``classifiers`` section is
used by PyPI to make it easier for new users to find your package, you can find a full list of classifiers `here
<https://pypi.org/classifiers/>`_. Likewise, the
``install_requires`` section specifies which Python packages that ``pip`` should
install before installing the package you are developing. Both these fields are
optional, so you can leave them blank until you have anything to fill in.

Lastly, the ``MANIFEST.in`` file. This file is used to instruct setupttools
on which files it should include when it creates an installable project. For
a general project, I reccomend having a file with the following layout.

.. code-block:: raw

   include setup.py
   include MANIFEST.in
   include LICENSE
   include README.md

   graft tests
   graft examples
   graft docs
   graft src

The ``requirements.txt`` file 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``requirements.txt`` file is similar to the ``install_requires`` field in
the ``setup.cfg`` file we described above. However, the aim of the
``requirements.txt`` file is not to specify the dependencies of your package,
but the packages needed to work on developing your package. Each dependency
should be on a separate line. Here is an example of a ``requirements.txt``
file.

.. code-block:: raw

   scikit-learn
   tox
   black
   isort
   -e .

We will depend on ``scikit-learn`` if we are to create scikit-learn compliant
code. Similarly, we need ``tox`` to run our test-suite. ``black`` and ``isort``
are two really good code auto-formatters, which you can read more about on
their GitHub pages (`black
<https://github.com/psf/black>`_ and `isort
<https://github.com/timothycrosley/isort>`_). Finally, with the ``-e .`` line
we install the current directory in editable mode.

The ``README.rst`` file
^^^^^^^^^^^^^^^^^^^^^^^^
The readme file contains the contens that are showed by default on online
source control providers such as GitHub, GitLab and BitBucket. Normally, this
is formatted as a Markdown file. However, I reccomend that you use
reStructuredText (rst) instead, since that is the file-format used by Sphinx,
the most commonly used auto-documentation tool for Python.

Additionally, PyPI will only host rst formatted help strings, not Markdown
formatted ones. Thus, if you wish to make your library public for ``pip``
installation in the future, then you should use rst to avoid writing the
same text twice.

The rst documentation is available `here
<http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`_, and a good
summary is available `here
<https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_.


The ``.gitignore`` file
^^^^^^^^^^^^^^^^^^^^^^^^

The ``.gitignore`` file contains instructions to Git, informing it of which
files it should not track. Examples of such files are the ``__pycache__`` files
and IDE configuration files. You can either copy the ``.gitignore`` file in this
repository, which should work for a large array of development environments, or
create your own ``.gitignore`` using `gitignore.io
<http://gitignore.io/>`_.

The ``LICENSE.txt`` file
^^^^^^^^^^^^^^^^^^^^^^^^

Your project needs an open source license, otherwise, noone will be able to use
your project. I like the MIT license, which is a very open license. To decide a 
license, i reccomend `choosealicense
<https://choosealicense.com/>`_ if
you are unsure as to which license to use.

Running tests with tox
^^^^^^^^^^^^^^^^^^^^^^

You should unit test your code. Otherwise there will be bugs, no matter how
simple the codebase is. The tool I like to use for unit testing is called
tox, and works by creating new virtual environments for each python version
you want to test the codebase with. It then installs all libraries necessary
to run the test suite before running it. These specifications are given in the
``tox.ini`` file, which can have the following structure

.. code-block:: ini

   [tox]
   envlist = 
      py35
      py36

   [testenv]
   deps =
      pytest
      pytest-cov
      pytest-randomly
   commands =
       pytest --cov=<package_name> --randomly-seed=1

The ``envlist`` field specifies which python versions to run the code with,
the ``deps`` field specifies the test dependencies (which might be different
from the devloper dependencies) and ``commands`` specifies which commands to
be ran to run the test suite.

NOTE: tox with conda
""""""""""""""""""""
Note that ``tox`` by itself doesn't play nice with ``conda``. Thus, if you
have an Anaconda or Miniconda installation of Python, then you should manually
install ``tox-conda`` through ``pip``.
    
Keeping the package source in the src folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have noticed that the source files are kept inside a separate ``src``
folder. The reason is that we should be certain that the code we are testing
is the installable code. To accomplish this, it is neccessary to structure the
code this way. For more information on this topic, see `this page
<https://hynek.me/articles/testing-packaging/#src>`_.

Keeping the tests in a tests folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the same reason as we keep the package source in the src folder, we keep the
unit tests in the tests folder.

Documenting the code with sphinx
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you publish code, you should also publish documentation to that code, and
creating the documentation is very simple if you have good docstrings and use
`sphinx
<http://www.sphinx-doc.org/en/master/>`_. To use sphinx, navigate to the docs
folder in the terminal window and type sphinx-quickstart.

We will not discuss sphinx in detail here, the only extra note I want to add
is to use the `sphinx.ext.napoleon` extension so your docstrings can be in the
`numpydoc
<https://github.com/numpy/numpydoc>`_ style.

Providing example code
^^^^^^^^^^^^^^^^^^^^^^

Any library should come with at least a minimal example script so prospective
users can see how the package was intended to be used. Keep these example
scripts in the examples folder.

Editable installs
-----------------
One immensely useful facet of the python ecosystem is editable installs. Often,
when new Python programmers create a project, they do not install the project
with pip. Rather, whenever they need to use the code from one project within
another, they end up manually modifying the system path environment variable.
If this sounds familiar, then you should stop that immediately. There is a
cleaner, easier and less error-prone way to accomplish the same. This way is
called editable installs.

Normally when we install a Python package, it is copied into the 
``site-packages`` directory. This is not ideal if the code we installed
is code that we are actively developing. In this case, we want to create a
symbolic link between the ``site-packages`` directory and the project
directory, and a way to accomplish this is through editable installs.

To installl a project in editable mode, simply navigate to the project root
directory and type ``pip install -e .`` in the terminal window. A benefit of
doing it this way, is that we have better cross-platform support. Windows and
UNIX based systems have vastly different ways of handling the path variable, so
your old ``sys.path.append`` hack might not work as intended on a Windows
machine. Additionally, the ``sys.path.append`` method is highly dependent on the
file-structure on your computer, whereas editable installs are not.


Automatic documentation
-----------------------

The second most important part of a project, after the source code itself, is
the documentation. Luckily, writing Python documentation is relatively painless
so long as you write your docstrings following the Sphinx guidelines. I will
assume that you have a working sphinx environment and simply want to host the
documentation somewhere.

If you are in this category, then you are in luck since you can host your
documentation for free on `Read the Docs
<https://readthedocs.org/>`_. To do this, you need to connect your GitHub
user to `https://readthedocs.org` (note the org top level domain (TLD), not
an io TLD). Once you have connected your GitHub to Read the Docs, you need
to add the ``.readthedocs.yml`` file to your repository. This file should have
the following lines in it.

.. code-block:: yaml

   python:
      setup_py_install: true

After adding the ``.readthedocs.yml`` file to the repository, it should have
the following layout.

.. code-block:: raw
   
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
   │   └── test_package_name
   │       └── __init__.py
   ├── .gitignore
   ├── .readthedocs.yml  <- This file is new
   ├── LICENSE.txt
   ├── MANIFEST.in
   ├── README.rst
   ├── requirements.txt
   ├── setup.cfg
   ├── setup.py
   └── tox.ini

Once it does, you can import the project to Read the Docs, by pressing the
"Import a Project" button and choosing the correct GitHub repository.

You might want to have a badge that shows whether your documentation builds
correctly on your GitHub page, to do this, press the "i" button on the right
of the green "docs passing" badge (or red "docs failing" if your documentation
isn't building correctly). Copy the rst code to somewhere near the beginning of your readme file. The code should be on the following form:

.. code-block:: raw

   .. image:: https://readthedocs.org/projects/<repo_name>/badge/?version=latest
      :target: https://<repo_name>.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status

Using continuous integration
----------------------------

Another useful tool when developing code is a continuous integration tool.
Such tools will automatically run the unit tests on activity to the GitHub
repository. Luckily, there exists a very good tool called `*Travis-CI*
<https://travis-ci.org/>`_, which is free for all open source projects.

To use Travis-CI, you must link your GitHub user to Travis CI on their webpage.
After this, you simply choose which repository to activate Travis for and you
are set to go. When you have activated Travis for a specific repo, you need
to add a ``.travis.yml`` file to the project root, giving you the following
file structure

.. code-block:: raw
   
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
   │   └── test_package_name
   │       └── __init__.py
   ├── .gitignore
   ├── .readthedocs.yml
   ├── .travis.yml  <- This file is new
   ├── LICENSE.txt
   ├── MANIFEST.in
   ├── README.rst
   ├── requirements.txt
   ├── setup.cfg
   ├── setup.py
   └── tox.ini

The contents of the ``.travis.yml`` file should be the following

.. code-block:: yaml

   sudo: false
   language: python
   python:
     - "3.7"
   # command to install dependencies
   install:
   before_script:
     - pip install tox-travis
   # command to run tests
   script: tox

This file will ensure that tox is run on Travis-CI any time someone pushes
a change to the GitHub repository. You might also want to add a badge to
your readme file. To do this, navigate to the Travis-CI dashboard, press
the link to the repository that you want to add the badge for, press the
badge showing ``build passing`` (ideally, it will show ``build failing``
if your tests are failing) and finally, choose rst from the bottom dropdown
menu. Once you have done this, copy the text in the text-box and paste it
somewhere around the top of yor ``README.rst`` file. The rst code that you
copy should look something like this

.. code-block:: rst

   .. image:: https://travis-ci.org/<github_username>/<repo_name>.svg?branch=<branch_name>
      :target: https://travis-ci.org/<github_username>/<repo_name>


Automatic coverage reporting
----------------------------

Another useful tool in a programmer's arsenal is automatic code coverage
reporting. Have you ever seen a repository where they have a badge that
shows how high their code-coverage is with a small badge? They accomplish
this using one of many automatic code-coverage reporters. Personally,
I like to use `*Coveralls*
<https://coveralls.io/>`_, which has a relatively easy-to-use interface
and integrates well with Travis-CI.

To start using Coveralls, you must first register and link your GitHub account
with Coveralls. Once you have done that, you need to add your repository to
Coveralls. You can do this, by pressing the plus button on the left-hand side of
the Coveralls dashboard and enable whichever repository you want. Once you have
done this, you must update the ``.travis.yml`` file so Coveralls are ran after
the test suite. The new ``.travis.yml`` file should look like this:

.. code-block:: yaml

   sudo: false
   language: python
   python:
     - "3.7"
   # command to install dependencies
   install:
   before_script:
     - pip install tox-travis
     - pip install coveralls
   # command to run tests
   script: tox
   after_success: coveralls

Once you have made this update, then Coveralls will run after travis. Next, you
want to add the coverage badge to your ``README.rst`` file. In the Coveralls
project dashboard, you should see a badge that displays your code coverage,
press the embed button on the top right corner near the badge and copy the
code for rst into your ``README.rst`` file. The code you copy should have
the following format

.. code-block:: rst

   .. image:: https://coveralls.io/repos/github/<github_username>/<repo_name>/badge.svg?branch=<branch_name>
      :target: https://coveralls.io/github/<github_username>/<repo_name>?branch=<branch_name>

Uploading to PyPI
-----------------
It is finally time to upload our code to PyPI, making it easily installable for
others. Uploading code to PyPI is very simple. First, create an account on PyPI.
Then, you need to install two packages; twine and wheel. To do this, write 
``pip install twine wheel`` in the terminal window. Then, navigate to the
project root and type ``python setup.py sdist bdist_wheel``, this will prepare
your package for uploading to PyPI. Then, write ``twine upload dist/*`` to
upload your project.

