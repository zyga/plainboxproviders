plainboxproviders
=================

Django application for indexing and searching all plainbox providers


Installation
============

You should run Ubuntu 14.04 (but really only tested on 14.10) with the latest version of python3-plainbox (from the ppa:checkbox-dev/ppa).

You will need python3 versions of python3-whoosh and python3-django-haystack that I've made. You cannot yet get them from the archive.
To get them you can rebuild my source packages: https://www.dropbox.com/sh/zvclxmbw8h9u4xk/AADIsl478hQm3VDrowaI2u9qa/packages or wait for
me to setup a PPA

The current code is insecure (session cookie secret is in the source code) and inefficient (both database and search engine are not
meant for larger deployments) but should be good for a local instance or a demo. Once you have the two special packages installed do this:

$ sudo apt-get install python3-django
$ ./manage.py syncdb
$ ./manage.py runserver

Now open http://localhost:8000/admin and log in with the username & password you've just created

Go to http://127.0.0.1:8000/admin/providerbackend/repository/add/ and add 'lp:checkbox' (bazaar), then 'lp:cdts' and 
lp:plainbox-provider-phablet (those are the currently known provider-hosting repositories). You can also add any additional
repositories you like, including local directories.

Now go to http://127.0.0.1:8000/admin/providerbackend/repository/ select all the repositories you've created, click on the action
combo box (above the first repository) and select 'Probe repository for providers'. This will block for a moment (it should
be started through celery but we don't have celery python3 support yet).

Now go back to shell and run ./manage.py update_index

Now you are all set.

You will need to repeat the two steps to update the database and the search index. There is no command-line command to re-probe proviers
yet and provider repository checkouts are not cached. This can be improved a lot.

Usage
=====

Open http://localhost:8000/ and search for anything you like!

Ideas
=====

1. Add detail pages for various objects
2. Add whitelist models
3. Add a 'authoritative' flag for repository to indicate that it holds "the best" version of a particular provider
4. When probing providers, validate each one and store the problems in a database. Show this on a provider detail page.
5. Show a list of flags used anywhere in any provider
6. Add a way to download a provider click package
7. Make this into pypi for providers? :-)


