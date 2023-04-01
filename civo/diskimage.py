import requests

from .utils import filter_list


class DiskImages:
    """
    Disk Images contains the contents and structure of a disk volume or of an entire data storage device on the Civo cloud platform.
    Note:Every region will have similar set of disk images. But the disk image IDs are different.
    """

    def __init__(self, headers, api_url,region):
        self.headers = headers
        self.url = '{}/v2/disk_images'.format(api_url)
        self.region = region

    def list(self) -> list:
        """
        Function to list available disk images available in a particular region
        :return: object json
        """
        params = {}
        if self.region:
            params = {
                "region":self.region
            } 
        r = requests.get(self.url, headers=self.headers,params=params)

        return r.json()
    
    def retrieve(self,disk_id:str)->dict:
        """
        Function to retrieve single disk image's details
        :param disk_id: Disk Id of disk of which image is to be retrieved(Note:This is region specific)
        :return: object json
        """
        params = {}
        if self.region:
            params = {
                "region":self.region
            } 
        r = requests.get(self.url+"/{}".format(disk_id),headers=self.headers,params=params)
        return r.json()

