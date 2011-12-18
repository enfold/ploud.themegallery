===================
ploud theme gallery
===================


Build
=====

Clone github repo::

  >> git clone git://github.com/fafhrd91/ploud.themegallery.git

Build app::

  >> cd ploud.themegallery
  >> python2.7 ./bootstrap.py -d
  >> ./bin/buildout -c devel.cfg


Start app
=========

Start wsgiref based service::

  >> ./bin/pserve development.ini


Default login/password: admin/12345


Plone client product
====================

https://github.com/collective/ploudenv.themegallery
