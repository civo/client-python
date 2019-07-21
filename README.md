# Civo python API Library

This project is the python API library for using in python projects.


```sh
pip install civo
```

## API Library

To use the library in your own python projects you can just add it to the requirements.txt:

```python
civo
```

Install the package:

```sh
pip install civo
```

You need to define `CIVO_TOKEN` in the environment or when you create a instance of `civo` you can pass the token.

Then you can use classes like this:

```python
from civo import Civo

civo = Civo('token')
ssh_file = open('~/.ssh/id_dsa.pub').read()

civo.ssh.create(name='default', public_key=ssh_file)
civo.instances.create(hostname='text.example.com', size='g2.xsmall', 
                      region='lon1', template_id='f80a1698-8933-414f-92ac-a36d9cfc4ac9',
                      public_ip='true', ssh_key='default')
```

The API library consists of a handful of classes that implement the Civo API. There is full documentation on the API available at https://api.civo.com/doc/.