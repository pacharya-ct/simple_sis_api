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

class SiteLabelGroup(APIBase):
    endpointurl = 'site-label-groups'
    allowed_multivalue_filters = []
    allowed_filters = APIBase.allowed_filters + ['groupname_icontains',
        'namespace', 'description_icontains', ]
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['namespace', 'groupname']

class SiteLabel(APIBase):
    endpointurl = 'site-labels'
    allowed_multivalue_filters = []
    allowed_filters = APIBase.allowed_filters + ['labelname_icontains',
        'namespace', 'description_icontains', ]
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['namespace', 'labelname']

class SiteLog(APIBase):
    endpointurl = 'site-logs'
    allowed_multivalue_filters = ['netcode', 'lookupcode', ]
    allowed_filters = APIBase.allowed_filters + ['subject_icontains',
        'logdate_gte', 'logdate_lte', 'logtype_icontains', 'author_icontains']
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['logtype', 'logdate']

class Site(APIBase):
    endpointurl = 'sites'
    allowed_multivalue_filters = ['netcode', 'lookupcode', ]
    allowed_filters = APIBase.allowed_filters + ['isactive']
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['network.netcode', 'lookupcode']

class Equipment(APIBase):
    endpointurl = 'equipment'
    allowed_multivalue_filters = ['category', 'categorygroup', 'modelname', 'serialnumber',
        'operatorcode', 'ownercode', 'inventory', 'equipmentid']
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['categorygroup', 'category', 'modelname', 'serialnumber']

class EquipmentCategory(APIBase):
    endpointurl = 'equipment-categories'
    allowed_multivalue_filters = ['category', 'categorygroup', ]
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['categorygroup', 'category', ]

class EquipmentModel(APIBase):
    endpointurl = 'equipment=models'
    allowed_multivalue_filters = ['category', 'categorygroup', 'modelname', 'family', ]
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['modelname', ]

class EquipmentLog(APIBase):
    endpointurl = 'equipment-logs'
    allowed_multivalue_filters = ['category', 'serialnumber',
        'operatorcode', ]
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = ['logdate_gte', 'logdate_lte',
        'subject_q', 'author_q']
    # Default values if applicable
    default_sort = ['logdate', 'subject']

class EquipmentProblem(APIBase):
    endpointurl = 'equipment-problems'
    allowed_multivalue_filters = ['category', 'serialnumber',
        'operatorcode', ]
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = ['isactive', 'ondate_gte', 'ondate_lte',
        'subject_q', 'author_q']
    # Default values if applicable
    default_sort = ['ondate', 'subject']

class Network(APIBase):
    endpointurl = 'networks'
    allowed_multivalue_filters = []
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    default_sort = []

class Organization(APIBase):
    endpointurl = 'organizations'
    allowed_multivalue_filters = []
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = ['namespace', 'orgcode_q']
    default_sort = ['orgcode']

class Place(APIBase):
    endpointurl = 'places'
    allowed_multivalue_filters = ['placename_icontains', ]
    allowed_filters = APIBase.allowed_filters + ['latitude_gte', 'latitude_lte',
        'longitude_gte', 'longitude_lte', ]
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['placename', ]

class TelemetryConnection(APIBase):
    endpointurl = 'telemetry-connections'
    allowed_multivalue_filters = ['connectiontype', 'category', 'modelname', 'serialnumber',
        'netcode', 'lookupcode', 'operatorcode']
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['conntype', 'ondate',]

class TelemetryNode(APIBase):
    endpointurl = 'telemetry-nodes'
    allowed_multivalue_filters = ['category', 'modelname', 'serialnumber',
        'netcode', 'lookupcode', 'operatorcode']
    allowed_filters = APIBase.allowed_filters + []
    allowed_client_filters = []
    # Default values if applicable
    default_sort = ['ondate',]
