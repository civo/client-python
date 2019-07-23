import os
import requests
from utils import filter_list


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
        self.networks = self.Networks(self.headers)
        self.snapshots = self.Snapshots(self.headers)
        self.volumes = self.Volumes(self.headers)
        self.firewalls = self.Firewall(self.headers)
        self.dns = self.Dns(self.headers)

    class Ssh:
        """
        To manage the SSH keys for an account that are used for logging in to instances,
        there are a set of APIs for listing the SSH public keys currently stored,
        as well as adding and removing them by name.
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

        def lists(self, filter: str = None) -> object:
            """
            Function to listing the SSH public keys
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

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
        Instances are running virtual servers on the Civo cloud platform. They can be of variable size.
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

        def lists(self, tags: str = None, page: str = None, per_page: str = None, filter: str = None) -> object:
            """
            Functikon to list all instances
            :param tags: a space separated list of tags, to be used freely as required.
                   If multiple are supplied, instances must much all tags to be returned (not one or more)
            :param page: which page of results to return (defaults to 1)
            :param per_page: how many instances to return per page (defaults to 20)
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
               you can filter by any object that is inside the json
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

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

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
        To manage the private networks for an account, there are a set of APIs for listing them, as well as adding,
        renaming and removing them by ID.
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

        def lists(self, filter: str = None) -> object:
            """
            Function to listing the private networks
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: [
                      {
                        "id": "50f2fffa-f81e-4e96-830f-e78f7e565e6f",
                        "name": "example-ltd-a775-development-75362452-562f-4b70-a65a-aeb4d4cd6864",
                        "region": "lon1",
                        "default": false,
                        "cidr": "0.0.0.0/0",
                        "label": "development"
                      }
                    ]
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

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

    class Snapshots:
        """
        We provide a backup service for our Instances called snapshots. This takes an exact copy of the instance's
        virtual hard drive. At any point an instance can be restored to the state it was in when the snapshot was made.
        These snapshots can also be used to build a new instance to scale identically configured infrastructure.

        As snapshot storage is chargeable, at any time these can be deleted. They can also be scheduled rather than
        immediately created, and if desired repeated at the same schedule each week (although the repeated snapshot
        will overwrite itself each week not keep multiple weekly snapshots).
        """

        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/snapshots'

        def create(self, name: str, instance_id: str, safe: str = 'false', cron_timing: str = None) -> object:
            """
            Function to create a new or update an old snapshot
            :param instance_id: The ID of the instance to snapshot
            :param name: The name of the instance
            :param safe: If true the instance will be shut down during the snapshot to ensure all files are in a
                         consistent state (e.g. database tables aren't in the middle of being optimised and hence
                         risking corruption). The default is false so you experience no interruption of service,
                         but a small risk of corruption.
            :param cron_timing: If a valid cron string is passed, the snapshot will be saved as an automated snapshot,
                                continuing to automatically update based on the schedule of the cron sequence provided.
                                The default is nil meaning the snapshot will be saved as a one-off snapshot.
            :return: objects json
            """
            payload = {'instance_id': instance_id}

            if safe:
                payload['safe'] = safe

            if cron_timing:
                payload['cron_timing'] = cron_timing

            r = requests.put(self.url + '/{}'.format(name), headers=self.headers, params=payload)

            return r.json()

        def lists(self, filter: str = None) -> object:
            """
            Function to list snapshots
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def delete(self, name: str) -> object:
            """
            Function to deleting a snapshot
            :param name: name of the instance
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(name), headers=self.headers)

            return r.json()

    class Volumes:
        """
        We provide a flexible size additional storage service for our Instances called volumes.
        This creates and attaches an additional virtual disk to the instance, allowing you to put backups or database
        files on the separate volume and later move the volume to another instance.

        As volume storage is chargeable, at any time these can be deleted.
        """

        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/volumes'

        def create(self, name: str, size_gb: str, bootable: str = 'false') -> object:
            """
            Function to create a new volume
            :param name: A name that you wish to use to refer to this volume (required)
            :param size_gb: A minimum of 1 and a maximum of your available disk space from your quota specifies
                            the size of the volume in gigabytes (required).
            :param bootable: Mark the volume as bootable with a boolean (optional; defaults to false).
            :return: objects json
            """
            payload = {'name': name, 'size_gb': size_gb}

            if bootable:
                payload['bootable'] = bootable

            r = requests.put(self.url + '/{}'.format(name), headers=self.headers, params=payload)

            return r.json()

        def lists(self, filter: str = None) -> object:
            """
            Function to list volumes
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def resizing(self, id: str, size_gb: str) -> object:
            """
            Function to resizing a volume
            :param id: id of the objects
            :param size_gb: A minimum of the existing size of the volume plus 1 and a maximum of your available
                            disk space from your quota specifies the size of the volume in gigabytes (required).
            :return: object json
            """
            payload = {'size_gb': size_gb}

            r = requests.put(self.url + '/{}/resize'.format(id), headers=self.headers, params=payload)

            return r.json()

        def attach(self, id: str, instance_id: str) -> object:
            """
            Function to attach a volume to an instance
            :param id: id of the objects
            :param instance_id: The ID of an instance that you wish to attach this volume to (required)
            :return: object json
            """
            payload = {'instance_id': instance_id}

            r = requests.put(self.url + '/{}/attach'.format(id), headers=self.headers, params=payload)

            return r.json()

        def detach(self, id: str) -> object:
            """
            Function to detach a volume from an instance
            :param id: id of the objects
            :return: object json
            """
            r = requests.put(self.url + '/{}/detach'.format(id), headers=self.headers)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to deleting a volume
            :param id: name of the instance
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

    class Firewall:
        """
        The simplest solution for most customers is to configure a firewall within their
        Instances using either iptables which is powerful or Uncomplicated Firewall/ufw
        which is much simpler but only works on Ubuntu.

        As an another option, customers can configure custom firewall rules for their
        instances using the Firewall API which adjusts the security group for your network
        of instances. These are a freely configurable option, however customers
        should be careful to not lock out their access to the instances.
        """

        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/firewalls'

        def create(self, name: str) -> object:
            """
            Function to create a new firewall
            :param name: A unique name for this firewall within your account
            :return: object json
            """
            payload = {'name': name}
            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def lists(self, filter: str = None) -> object:
            """
            Function to list firewalls
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to deleting a firewall
            :param id: id of the firewall object
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

        def create_rule(self, id: str, start_port: str, protocol: str = 'tcp', end_port: str = None, cidr: str = '0.0.0.0/0',
                   direction: str = 'inbound', label: str = None) -> object:
            """
            An account holder can create firewall rules for a specific firewall, but there is a quota'd limit
            to the number of rules that can be created, but generally this is much higher than most customers
            will require and it can be increased if required.
            :param id: Firewall id object
            :param protocol: the protocol choice from tcp, udp or icmp (the default if unspecified is tcp)
            :param start_port: the start of the port range to configure for this rule (or the single port if required)
            :param end_port: the end of the port range (this is optional, by default it will only apply to the single
                   port listed in start_port)
            :param cidr: the IP address of the other end (i.e. not your instance) to affect, or a valid network CIDR
                         (defaults to being globally applied, i.e. 0.0.0.0/0)
            :param direction: will this rule affect inbound or outbound traffic (by default this is inbound)
            :param label: a string that will be the displayed name/reference for this rule (optional)
            :return: object json
            """
            payload = {'protocol': protocol, 'start_port': start_port, 'cidr': cidr, 'direction': direction}

            if end_port:
                payload['end_port'] = end_port

            if label:
                payload['label'] = label

            r = requests.post(self.url + '/{}/rules'.format(id), headers=self.headers, params=payload)

            return r.json()

        def lists_rule(self, id: str, filter: str = None) -> object:
            """
            Function to list firewalls rules
            :param id: Firewall id object
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url + '/{id}/rules'.format(id), headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def delete_rule(self, id: str, rule_id: str) -> object:
            """
            Function to deleting a firewall rule
            :param id: id of the firewall object
            :param rule_id: id of the firewall rule object
            :return: object json
            """
            r = requests.delete(self.url + '/{}/rules/{}'.format(id, rule_id), headers=self.headers)

            return r.json()

    class Dns:
        """
        We host reverse DNS for all instances automatically. If you'd like to manage forward (normal)
        DNS for your domains, you can do that for free within your account. This API is effectively split
        in to two parts: 1) Managing domain names themselves, and 2) Managing records within those domain names.
        We don't offer registration of domains names, this is purely for hosting the DNS.
        If you're looking to buy a domain name, we recommend LCN.com for their excellent friendly support
        and very competitive prices.
        """
        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/dns'

        def create(self, name: str) -> object:
            """
            Function to setup a new domain
            :param name: the domain name, e.g. "example.com"
            :return: object json
            """
            payload = {'name': name}
            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def update(self, id: str, name: str) -> object:
            """
            Function to update a new domain
            :param name: the domain name, e.g. "example.com"
            :return: object json
            """
            payload = {'name': name}
            r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

            return r.json()

        def lists(self, filter: str = None) -> object:
            """
            Function to list all dns domains
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def delete(self, id: str) -> object:
            """
            Function to deleting a domain
            :param id: id of the domain object
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

        def create_record(self, id: str, type: str, name: str, value: str, priority: str, ttl: str = '600') -> object:
            """
            Function to create a new DNS record
            :param id: id of the domain object
            :param type: the choice of RR type from (a, cname, mx or txt)
            :param name: the portion before the domain name (e.g. www) or an @ for the apex/root domain
                         (you cannot use an A record with an amex/root domain)
            :param value: the IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
            :param priority: useful for MX records only, the priority mail should be attempted it (defaults to 10)
            :param ttl: how long caching DNS servers should cache this record for, in seconds
                        (the minimum is 600 and the default if unspecified is 600)
            :return: object json
            """
            payload = {'type': type, 'name': name, 'value': value, 'priority': priority, 'ttl': ttl}
            r = requests.post(self.url + '{}/records'.format(id), headers=self.headers, params=payload)

            return r.json()

        def update_record(self, id: str, id_record: str, type: str = None, name: str = None, value: str = None,
                          priority: str = None,
                          ttl: str = None) -> object:
            """
            Function to update a DNS record
            :param id: id of the domain object
            :param id_record: id of the record domain object
            :param type: the choice of RR type from (a, cname, mx or txt)
            :param name: the portion before the domain name (e.g. www) or an @ for the apex/root domain
                         (you cannot use an A record with an amex/root domain)
            :param value: the IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
            :param priority: useful for MX records only, the priority mail should be attempted it (defaults to 10)
            :param ttl: how long caching DNS servers should cache this record for, in seconds
                        (the minimum is 600 and the default if unspecified is 600)
            :return: object json
            """
            payload = {}

            if type:
                payload['type'] = type

            if name:
                payload['name'] = name

            if value:
                payload['value'] = value

            if priority:
                payload['priority'] = priority

            if ttl:
                payload['ttl'] = ttl

            r = requests.put(self.url + '{}/records/{}'.format(id, id_record), headers=self.headers, params=payload)

            return r.json()

        def lists_record(self, id: str, filter: str = None) -> object:
            """
            Function to list DNS records
            :param id: Firewall object id
            :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                           you can filter by any object that is inside the json
            :return: object json
            """
            r = requests.get(self.url + '{}/records'.format(id), headers=self.headers)

            if filter:
                data = r.json()
                return filter_list(data=data, filter=filter)

            return r.json()

        def delete_record(self, id: str, record_id: str) -> object:
            """
            Function to deleting a dns record
            :param id: id of the dns object
            :param record_id: id of the dns record object
            :return: object json
            """
            r = requests.delete(self.url + '/{}/records/{}'.format(id, record_id), headers=self.headers)

            return r.json()
