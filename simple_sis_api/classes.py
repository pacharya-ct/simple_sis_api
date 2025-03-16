'''
classes.py
Author: Prabha Acharya
Create date: 20240402
Version: 0.1
'''

from simple_sis_api import APIBase

class SiteEpoch(APIBase):
    endpointurl = 'site-epochs'
    allowed_multivalue_filters = ['netcode', 'lookupcode', 'operatorcode']
    allowed_filters = APIBase.allowed_filters + ['isactive', 'latitude_gte', 'latitude_lte', 
        'longitude_gte', 'longitude_lte', ]
    allowed_client_filters = ['sitetypes_q', 'telemetrytypes_q', 
        'ondate_gte', 'ondate_lte', 'offdate_gte', 'offdate_lte']
    # Default values if applicable
    default_sort = ['netcode', 'lookupcode']

class EquipmentInstallation(APIBase):
    endpointurl = 'equipment-installations'
    allowed_multivalue_filters = ['category', 'categorygroup', 'modelname', 'serialnumber', 
        'netcode', 'lookupcode']
    allowed_filters = APIBase.allowed_filters + ['isactive', 'ondate_gte', ]
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['categorygroup', 'category', 'modelname', 'serialnumber']

    def custom_sort(self, filtered_data):
        # sort by seismic equipment first and then the rest.
        seismic = []
        nonseismic = []
        for entry in filtered_data:
            if entry['categorygroup'] == 'SEISMIC-EQUIPMENT':
                seismic.append(entry)
            else:
                nonseismic.append(entry)

        custom_sorted = seismic + nonseismic
        return custom_sorted

