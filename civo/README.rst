Civo

This project is the python API library for using in python projects.

Usage
-----
>>> from civo import Civo
>>> civo = Civo('token')
>>> ssh_file = open('~/.ssh/id_dsa.pub').read()

>>> civo.ssh.create(name='default', public_key=ssh_file)
>>> civo.instances.create(hostname='text.example.com', size='g2.xsmall',
                      region='lon1', template_id='f80a1698-8933-414f-92ac-a36d9cfc4ac9',
                      public_ip='true', ssh_key='default')


Installation
------------
pip3 install civo

Requirements
^^^^^^^^^^^^
requests

Compatibility
-------------
python 3.7

Licence
-------
Mit License

Authors
-------

`civo` was written by `Alejandro JNM <alejandrojnm@gmail.com>`_.