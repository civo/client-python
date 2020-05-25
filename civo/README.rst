Civo

This project is the python API library for using in python projects.

Usage
-----
>>> from civo import Civo
>>> from os.path import expanduser
​
>>> civo = Civo('token')
>>> home = expanduser("~/.ssh/")
>>> ssh_file = open('{}id_dsa.pub'.format(home)).read()
​
>>> # you can filter the result
>>> size_id = civo.size.search(filter_by='name:g2.xsmall')[0]['name']
>>> template = civo.templates.search(filter_by='code:debian-stretch')[0]['id']
​
>>> civo.ssh.create(name='default', public_key=ssh_file)
>>> ssh_id = civo.ssh.search(filter_by='name:default')[0]['id']
>>> civo.instances.create(hostname='text.example.com', size=size_id,
                      region='lon1', template_id=template,
                      public_ip='true', ssh_key=ssh_id)


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