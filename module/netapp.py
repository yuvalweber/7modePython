from base64 import b64encode
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import requests
import xmltodict
import re

class Controller:
    def __init__(self,controller,username,password):
        self.controller = controller
        self.username = username
        self.password = password
        session = requests.Session()
        creds_to_encode = "{}:{}".format(username,password).encode()
        encoded_creds = b64encode(creds_to_encode).decode()
        headers = {"Authorization":"Basic {}".format(encoded_creds),"Content-Type": "application/x-www-form-urlencoded","Host": controller,"Connections": "Close"}
        session.headers.update(headers)
        self.session = session
        self.url = "http://{}/servlets/netapp.servlets.admin.XMLrequest_filer".format(controller)

    def get_volumes(self):
        root = Element('netapp',version='1.0',xmlns='http://www.netapp.com/filer/admin')
        vol_info_child = SubElement(root, "volume-list-info-iter-start")
        verbose_sub_child = SubElement(vol_info_child,"verbose")
        verbose_sub_child.text = "true"
        data = tostring(root) 

        response = self.session.post(self.url,data=data)
        dict_response = xmltodict.parse(response.text)
        tag = dict_response['netapp']['results']['tag']
        volumes = {}

        second_root = Element('netapp',version='1.0',xmlns='http://www.netapp.com/filer/admin')
        vol_info_iter_child = SubElement(second_root,"volume-list-info-iter-next")
        maximum_sub_child = SubElement(vol_info_iter_child,"maximum")
        maximum_sub_child.text = "20000"
        tag_sub_child = SubElement(vol_info_iter_child,"tag")
        tag_sub_child.text = tag
        data = tostring(second_root)

        response = self.session.post(self.url,data=data)
        dict_response = xmltodict.parse(response.text)
        volumes_loop = dict_response['netapp']['results']['volumes']['volume-info']
        for volume in volumes_loop:
            name = volume['name']
            volume.pop('name',None)
            volumes[name] = volume
        return volumes
    
    def get_snapshots(self,volume_name):
        root = Element('netapp',version='1.0',xmlns='http://www.netapp.com/filer/admin')
        snapshot_list_child = SubElement(root,"snapshot-list-info")
        snapowners_sub_child = SubElement(snapshot_list_child,"snapowners")
        snapowners_sub_child.text = "true"
        target_name_sub_child = SubElement(snapshot_list_child,"target-name")
        target_name_sub_child.text = volume_name
        target_type_sub_child = SubElement(snapshot_list_child,"target-type")
        target_type_sub_child.text = "volume"
        data = tostring(root)

        response = self.session.post(self.url,data=data)
        dict_response = xmltodict.parse(response.text)
        snapshots = {}
        snapshots_loop = dict_response['netapp']['results']['snapshots']['snapshot-info']
        for snapshot in snapshots_loop:
            name = snapshot['name']
            snapshot.pop('name',None)
            snapshots[name] = snapshot
        return snapshots