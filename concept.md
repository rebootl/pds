pds - personal documentation system

Purpose
-------

Distributed content[^1] shall be collected and prepared into an appealing
form.

Primarly the content shall be prepared for a web browser.
Secondary output formats shall be possible.

Usage as a simple static website generator (CMS) should be possible too.

[^1]: Originally the intention was for content distributed on one filesystem
(machine). By using git, the content can basically be distributed pretty much
anywhere.
(Though the repos should be accessible directly. Really?)


The content shall be stored in bare git repositories. Those repos shall
be placed in a designated folder.


Workflow
--------

1) The idea is that one can simply create a new folder somewhere, for a project,
   notes, articles or whatever. Then this folder can be git-initialized and a
   bare repo, in a designated folder, is to be created.
   (This is pure git functionality, though a convenience function for the first
   init and bare repo creation may be provided.
   However, _after_ the first initialization and bare repo creation the folder
   and its content shall be managed purely by git.)

Creating bare repos, basically means a git server is set-up! That means that
these repos can be checked out and updated from anywhere. Provided access to
the server, of course. Even a git web interface could be used to update/edit
content, analog to a so called back-end in a common CMS.

2) From this bare repos the pds updates/prepares its output into another
   designated folder.
   (Updating may be fully automated by using git hooks in the bare repos e.g.
   when pushing on a repo.)

Only defined git branches, by default public, private and preview, will be used
for processing.

These branches are separated into different output directories.


Layout
------

The resulting site can be viewed as the following separate parts:

A) The content of the respective page.

B) The site layout in which the pages are embedded.

These are brought toghether by using a pandoc template.

A "special" repository, by default called base-layout, shall provide
the basic layout of the page. E.g. the "home" page, CSS style-sheets,
Javascript files, Background images etc..
In case a simple website shall be created all the content can be put in
there.


Content
-------

Page content is processed directory wise.

All markdown files found, identified by a defined extension, will be 
processed using Pandoc.

Ordering by numbers and then letters, the first (markdown) file found 
will be used as _index.html_.

A plugin system is provided to extend the pandoc functionality.
Further a custom math processing is implemented (using ?...?).

In the first implementation an output as PDF for single pages, shall
be possible.
Other output formats or different grouping may be implemented later.

Plugins _need_ to provide output for the other formats as well.


Menus
-----

Based on the content of the base-layout one __main menu__ is created.
Those items may as well be defined in a config file.
? or in the template ?

This menu contains directories and subdirectories linking to their
index.html.

A __repository menu__, containing the other repositories, shall be provided.
Again subdirectories shall appear.

And finally a __pages menu__ is created, linking to all the markdown files in 
the active directory.

The active menu item shall receive a defined "active" CSS style.

Single pages, identified by keywords in their filename, may be excluded
from menu processing.
