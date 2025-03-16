'''
base.py
Author: Prabha Acharya
Create date: 20240402
Version: 0.1

'''

import requests
import os
from collections import defaultdict
import logging
import simple_sis_api as ssa

logger = logging.getLogger(__name__)

class APIBase(object):
    '''
    Base class to access the SIS webservice endpoints. 
    Contains functions to fetch data over multiple pages, apply client side filters, 
    flatten the nested structure, merge the included data and return a python dictionary
    '''

    logger = logger
    
    # Define the following class attrs in subclasses
    endpointurl = None      
    # all possible multivalue filters for this endpoint used as a list. 
    allowed_multivalue_filters = []
    # all possible single value filters for this endpoint. 
    allowed_filters = ['page[number]', 'sort']
    allowed_client_filters = []
    # Default values if applicable
    default_filters = {'page[number]': 1, }
    default_sort = []

    def __init__(self, baseurl, tokenfp):
        self.baseurl = baseurl
        with open (tokenfp) as f:
            content = f.read()
            token = content.strip()

        # Set the token to be used in the request header
        self.auth_header = {'Authorization': f'Bearer {token}',}

    def get_filtered_list(self, filterby, sortby=[]):
        ''' 
        Sends a request to a list API endpoint and 
        returns filtered results in a flattened format
        Returns a list of dict objects
        '''
        filterparams = dict(self.default_filters)
        sortby = sortby if sortby else self.default_sort
        if sortby:
            filterparams['sort'] = ','.join(sortby)
        client_filters = {}
        for k, v in filterby.items():
            if k in self.allowed_multivalue_filters:
                if type(v) == list:
                    filterparams[k] = ','.join(v)
                else:
                    filterparams[k] = v
            elif k in self.allowed_filters:
                filterparams[k] = v
            elif k in self.allowed_client_filters:
                client_filters[k] = v
            else:
                self.logger.debug(f'Filter param "{k}" not supported by endpoint {self.endpointurl}')

        all_data, incl_data = self._get_all_pages(**filterparams)

        if all_data is None:
            return

        incl_elems = self._flatten_data(incl_data)
        # convert into lookup dict where key is (type, id)
        lookup_map = {}
        for e in incl_elems:
            t = e.pop('type')
            id = e.pop('id')
            lookup_map[(t, id)] = e

        elem_list = self._flatten_data(all_data, lookup_map)
        filtered_data = [ elem for elem in elem_list if self._filter_data(elem, client_filters) ]
        sorted_data = self.custom_sort(filtered_data)
        return sorted_data

    def get_by_id(self, id, flatten=True):
        ''' Get the detail page for given id '''
        res = self._send_request(id=id)
        if flatten:
            elem_list = self._flatten_data([res['data']])
            return elem_list[0]
        else:
            return res['data']

    def custom_sort(self, filtered_data):
        # override in the sub classes to implement a custom sort that is not supported by the SIS API
        return filtered_data

    def _send_request(self, filterkw=None, id=None):
        url = f'{self.baseurl}/{self.endpointurl}'
        logger.info (f'Sending a request to {url} with filter: {filterkw} or id: {id}')
        if id:
            url = f'{url}/{id}'
        r = requests.get(url, headers=self.auth_header, params=filterkw, )
        r.raise_for_status()
        res = r.json()
        return res

    def _get_all_pages (self, **filterkw):
        ''' 
        Builds and sends the request and gets all the pages of data.
        Use filterkw to take advantage of server side filtering and to reduce extra large results.
        If a huge resultset is expected, add code to handle errors 
        that might be raised because of server side throttling.
        '''

        # Initialize a list to store the data entries fetched over multiple requests
        all_data = []
        incl_data = []        
        while (True):
            res = self._send_request(filterkw=filterkw)
            all_data.extend(res['data'])
            incl = res.get('included', None)
            if incl:
                incl_data.extend(incl)

            number_of_pages = res['meta']['pagination']['pages']

            # Go to the next page. Use this method, or look under links > next for the url.
            filterkw['page[number]'] += 1
            if filterkw['page[number]'] > number_of_pages:
                break
        
        return all_data, incl_data

    def _flatten_data(self, data, lookup={}):
        '''
        Takes in the json data element of form: 
            [{type: <type>, id:<id> attributes: { dict of attribs }, relationships: {}, links: {} }
        Extracts the type, id and everything under attributes, ignores relationships and links.
        For columns defined in ATTR_DATATYPE_MAPPING, cast the values using the data type
        Returns: elem_list: [ { type : <type>, id: int(<id>), attr1: <val1>, attr2: <val2> ..}]
        '''
        elem_list = []
        for elem in data:
            elem_detail = {'type' : elem['type'], 
                           'id': int(elem['id']) }

            for attr, val in elem['attributes'].items():
                if attr in ssa.ATTR_DATATYPE_MAPPING and val is not None:
                    # cast the val to the datatype defined in ATTR_DATATYPE_MAPPING
                    try:
                        val = ssa.ATTR_DATATYPE_MAPPING[attr](val)
                    except Exception as e:
                        logger.warning(f'Unable to cast {attr} value {val} to {ssa.ATTR_DATATYPE_MAPPING[attr]}. Error: {e}')
                elem_detail[attr] = val

            if lookup:
                for rel, reldict in elem['relationships'].items():
                    if 'meta' in reldict:
                        # generally present for many to many relations. 
                        # not supported right now
                        continue

                    d = reldict['data']
                    lookup_key = (d['type'], int(d['id']))
                    if lookup_key in lookup:
                        # do not overwrite any keys already present. 
                        # E.g. ondate is present in many objects, do not overwrite 
                        # the root object's ondate with the one from the lookup table
                        for lk, lkval in lookup[lookup_key].items():
                            if lk not in elem_detail:
                                elem_detail[lk] = lkval

            elem_list.append(elem_detail)
        return elem_list

    def _filter_data(self, elem, filterkw):
        ''' 
        Client side filtering 
        '''
        filters = []
        matched = True
        # For now all filterkw keys are expected to be in the allowed list, 
        # but that might not be the case if filters are chained.
        # Hence repeat the check to see if filter is supported by this class
        for k, val in filterkw.items():
            if k in self.allowed_client_filters:
                filters.append ((k, val))

        # No client filters, return
        if not filters:
            return matched

        for k, val in filters:
            filterkey, filtertype = k.split('_')
            elem_val = elem[filterkey]
            if filterkey == 'offdate' and elem_val is None:
                elem_val = ssa.FUTURE_OFF_DATE

            if filterkey in ssa.ATTR_DATATYPE_MAPPING and type(val) == str:
                val = ssa.ATTR_DATATYPE_MAPPING[filterkey](val)

            # Filters are ANDed implicitly. Check for failing condition and break out if match fails
            if filtertype is None:
                # cases insensitive search
                if val.lower() != elem_val.lower():
                    matched = False
                    break 

            elif filtertype == 'q':
                if val.lower() not in elem_val.lower():
                    matched = False
                    break

            elif filtertype == 'gte':
                if val > elem_val:
                    matched = False
                    break

            elif filtertype == 'lte':
                if val < elem_val:
                    matched = False
                    break
        return matched


