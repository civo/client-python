import os
import requests


class Civo:

    def __init__(self, civo_token: str = None):
        """
        Init for Civo class
        :param civo_token: str, optional the token generate by civo
        """

        # Get token from env or pass to the class
        if not civo_token:
            self.token = os.getenv('CIVO_TOKEN', False)
        else:
            self.token = civo_token

        # Create headers for all requests to civo api
        if not self.token:
            raise Exception('CIVO_TOKEN not found in the enviroment or is not declared in the class')

        self.headers = {'Authorization': 'bearer {}'.format(self.token)}

        # Ssh class
        self.ssh = self.Ssh(self.headers)
        self.instances = self.Instances(self.headers)

    class Ssh:
        """
        Class to handle all ssh operation
        """
        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/sshkeys'

        def create(self, name: str, public_key: str) -> object:
            """
            Function to uploading a SSH public key
            :param name: Name of the key
            :param public_key: Public key of the ssh
            :return: object json
            """
            payload = {'name': name, 'public_key': public_key}
            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def list(self) -> object:
            """
            Function to listing the SSH public keys
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            return r.json()

        def retrieving(self, id: str) -> object:
            """
            Function to retrieving a SSH key
            :param id: id of the objects
            :return: object json
            """
            r = requests.get(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

        def updating(self, id: str, name: str) -> object:
            """
            Function to updating a SSH key
            :param id: id of the objects
            :param name: name to change
            :return: object json
            """
            payload = {'name': name}
            r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to removing a SSH key
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

    class Instances:
        """
        Class to handle all instances operation
        """
        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/instances'

        def create(self, hostname: str, size: str, template_id: str, reverse_dns: str = None, region: str = None,
                   public_ip: str = 'create', move_ip_from: str = None, count: int = 1, network_id: str = None,
                   snapshot_id: str = None, initial_user: str = None, ssh_key_id: str = None, tags: str = None) -> object:
            """
            Function to create instance
            :param hostname: a fully qualified domain name that should be set as the instance's hostname (required)
            :param size: the identifier for the size, from the current list (required)
            :param template_id: the ID for the template to use to build the instance, from the current templates.
                   Parameter also accepted as template. (optional; but must be specified if no snapshot is specified)
            :param reverse_dns: a fully qualified domain name that should be used as the instance's IP's reverse DNS (optional, uses the hostname if unspecified)
            :param region: the identifier for the region, from the current region (optional; a random one will be picked by the system)
            :param public_ip: this should be either none, create or from. If from is specified then the move_ip_from
                   parameter should also be specified (and contain the ID of the instance that will be releasing its IP).
                   As aliases true will be treated the same as create and false will be treated the same as none.
                   If create or true is specified it will automatically allocate an initial public IP address,
                   rather than having to add the first one later (optional; default is create)
            :param move_ip_from: parameter should also be specified (and contain the ID of the instance that will be releasing its IP).
            :param count: the number of instances to create (optional, default is 1)
            :param network_id: this must be the ID of the network from the network listing (optional;
                   default network used when not specified)
            :param snapshot_id: the ID for the snapshot to use to build the instance, from your snapshots
                   (optional; but must be specified if no template is specified)
            :param initial_user: the name of the initial user created on the server
                   (optional; this will default to the template's default_username and fallback to "civo")
            :param ssh_key_id: the ID of an already uploaded SSH public key to use for login to the default user
                   (optional; if one isn't provided a random password will be set and returned in the initial_password field)
            :param tags: a space separated list of tags, to be used freely as required (optional)
            :return: objects json
            """

            payload = {'hostname': hostname, 'size': size, 'template_id': template_id}

            if reverse_dns:
                payload['reverse_dns'] = reverse_dns

            if region:
                payload['region'] = region

            if public_ip:
                payload['public_ip'] = public_ip

            if move_ip_from:
                payload['move_ip_from'] = move_ip_from

            if count:
                payload['count'] = count

            if network_id:
                payload['network_id'] = network_id

            if snapshot_id:
                payload['snapshot_id'] = snapshot_id

            if ssh_key_id:
                payload['ssh_key_id'] = ssh_key_id

            if initial_user:
                payload['initial_user'] = initial_user

            if tags:
                payload['tags'] = tags

            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def list(self, tags: str = None, page: str = None, per_page: str = None) -> object:
            """
            Functikon to list all instances
            :param tags: a space separated list of tags, to be used freely as required.
                   If multiple are supplied, instances must much all tags to be returned (not one or more)
            :param page: which page of results to return (defaults to 1)
            :param per_page: how many instances to return per page (defaults to 20)
            :return: objects json
            """
            payload = {}

            if tags:
                payload['tags'] = tags

            if page:
                payload['page'] = page

            if per_page:
                payload['per_page'] = per_page

            r = requests.get(self.url, headers=self.headers, params=payload)

            return r.json()

        def retrieving(self, id: str) -> object:
            """
            Function to retrieving a single instance
            :param id: id of the objects
            :return: object json
            """
            r = requests.get(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

        def retagging(self, id: str, tags: str) -> object:
            """
            Function to retagging an instance
            :param id: id of the objects
            :param tags: a space separated list of tags, to be used freely as required (optional)
            :return: object json
            """
            payload = {'tags': tags}

            r = requests.put(self.url + '/{}/tags'.format(id), headers=self.headers, params=payload)

            return r.json()

        def rebooting(self, id: str, type_reboot: str) -> object:
            """
            Function to rebooting an instance
            :param id: id of the objects
            :param type_reboot: (reboots|hard_reboots|soft_reboots)
            :return: object json
            """
            r = requests.post(self.url + '/{}/{}'.format(id, type_reboot), headers=self.headers)

            return r.json()

        def stop(self, id: str) -> object:
            """
            Function to shutting down an instance
            :param id: id of the objects
            :return: object json
            """
            r = requests.put(self.url + '/{}/stop'.format(id), headers=self.headers)

            return r.json()

        def start(self, id: str) -> object:
            """
            Function to starting an instance after being shut down
            :param id: id of the objects
            :return: object json
            """
            r = requests.put(self.url + '/{}/start'.format(id), headers=self.headers)

            return r.json()

        def resizing(self, id: str, size: str) -> object:
            """
            Function to upgrading (resizing) an instance
            :param id: id of the objects
            :param size: the identifier for the size, from the current list
            :return: object json
            """
            payload = {'size': size}

            r = requests.put(self.url + '/{}/resize'.format(id), headers=self.headers, params=payload)

            return r.json()

        def firewall(self, id: str, firewall_id: str = None) -> object:
            """
            Function to setting the firewall for an instance
            :param id: id of the objects
            :param firewall_id: the ID of the firewall to use, from the current list. If left blank or not sent,
                   the default firewall will be used (open to all)
            :return: object json
            """
            payload = {}

            if firewall_id:
                payload['firewall_id'] = firewall_id

            r = requests.put(self.url + '/{}/firewall'.format(id), headers=self.headers, params=payload)

            return r.json()

        def moving_ip(self, id: str, ip: str) -> object:
            """
            Function to moving a public IP between instances
            :param id: id of the objects
            :param ip: ip address
            :return: object json
            """
            r = requests.put(self.url + '/{}/ip/{}'.format(id, ip), headers=self.headers)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to deleting an instance
            :param id: id of the objects
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

    class Networks:
        """
        Class to handle all Networks operation
        """
        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/networks'

        def create(self, label: str) -> object:
            """
            Function to create a private network
            :param label: a string that will be the displayed name/reference for the network.
            :return: object json
            """
            payload = {'label': label}
            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def list(self) -> object:
            """
            Function to listing the private networks
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            return r.json()

        def rename(self, id: str, label: str) -> object:
            """
            Function to renaming a network
            :param id: id of the objects
            :param label: the new label to use.
            :return: object json
            """
            payload = {'label': label}
            r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to removing a private network
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()
