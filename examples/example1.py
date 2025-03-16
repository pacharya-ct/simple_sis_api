'''
example1.py
Author: Prabha Acharya
Create date: 20250314
Version: 0.1

Examples show how to use functions to add 
fixed queries and multi-step queries to get data

'''

import logging
import datetime as dt
import os
import argparse
from configparser import ConfigParser
from simple_sis_api import SiteEpoch, EquipmentInstallation

logger = None

def sitesActiveAsOfDate(se, theDate, **kw):
    filterkw = dict(kw)
    filterkw['ondate_lte'] = theDate
    filterkw['offdate_gte'] = theDate
    return se.get_filtered_list(filterkw)

def activeSitesInstalledAfter(se, ondate, **kw):
    filterkw = dict(kw)
    filterkw['ondate_gte'] = ondate
    filterkw['isactive']="yes"
    return se.get_filtered_list(filterkw)

def getSitesNearSite(se, netcode, lookupcode, isactive='yes'):
    filterkw = dict(netcode=netcode, lookupcode=lookupcode)
    if isactive != 'all':
        filterkw['isactive']=isactive

    sites = se.get_filtered_list(filterkw)
    numsites = len(sites)
    if not sites:
        logger.warning (f'No site found for {netcode} {lookupcode}')
        return []

    if numsites > 1:
        logger.warning(f'Expecting one site but fetched {numsites}. Using first site from list of sites {sites[0]}')

    site = sites[0]
    lat = site['latitude']
    lon = site['longitude']

    bbkw = dict (latitude_lte=lat+0.5, latitude_gte=lat-0.5, 
                longitude_lte=lon+0.5, longitude_gte=lon-0.5 )

    # use all the params as filterkw, except for lookupcode
    bbkw.update(filterkw)
    bbkw.pop('lookupcode', None)

    nearbysites = se.get_filtered_list(bbkw)
    return nearbysites

def currentlyInstalledEquipAtNet(ei, netcode, **kw):
    filterkw = dict(kw)
    filterkw['isactive']='yes'
    filterkw['netcode']=netcode
    return ei.get_filtered_list(filterkw)

def get_unique_logger_models(ei, netcode):
    kw = dict (netcode=netcode, category='LOGGER')
    installed_loggers = ei.get_filtered_list(kw)
    
    loggermodels = []
    for equip in installed_loggers:
        if equip['modelname'] not in loggermodels:
            loggermodels.append(equip['modelname'])

    return loggermodels

def main():
    examples = dict(s1='CO Sites Active as of 2017-09-21',
                    s2='BK sites installed since 2024-03-01',
                    s3='Sites near CI WWF',
                    e1='Q8 loggers installed at CI stations',
                    e2='Installed equipment at CI WWF')

    parser = argparse.ArgumentParser(description='Wrapper for running various examples for simple_sis_api')
    parser.add_argument('inifile', help='Path and name of ini file')
    parser.add_argument('mode', choices=['test', 'prod'], help='Connect to sis test or prod site')
    parser.add_argument('example', choices=examples.keys(), 
                        help=', '.join([ f'{k}: {v}' for k, v in examples.items()]) )
    
    options = parser.parse_args()

    # Create the console logger 
    logger = logging.getLogger('simple_sis_api')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(ch)

    inifpath = options.inifile
    if not os.path.exists(inifpath):
        parser.error(f'ini file {inifpath} does not exist.')

    config = ConfigParser()
    config.read(inifpath)

    try:
        baseurl = config.get(options.mode, 'sis_api_url')
        tokenfp = config.get(options.mode, 'token_filepath')
        se = SiteEpoch(baseurl, tokenfp)
        ei = EquipmentInstallation(baseurl, tokenfp)
        sites = []
        equipinstalls = []
        if options.example == 's1':
            theDate = dt.datetime(2017, 9, 21, tzinfo=dt.UTC)
            sites = sitesActiveAsOfDate(se, theDate, netcode='CO')
        elif options.example == 's2':
            # Get active sites whose ondate is on or after 2024-03-01 for the BK network
            ondate = dt.datetime(2024, 3, 1, tzinfo=dt.UTC)
            sites = activeSitesInstalledAfter(se, ondate, netcode='BK')
        elif options.example == 's3':
            sites = getSitesNearSite(se, netcode='CI', lookupcode='WWF')
        elif options.example == 'e1':
            equipinstalls = currentlyInstalledEquipAtNet(ei, netcode='CI', category='LOGGER', modelname='Q8')
        elif options.example == 'e2':
            equipinstalls = currentlyInstalledEquipAtNet(ei, netcode='CI', lookupcode='WWF')

        print (f'Results for {options.example}: {examples[options.example]}')
        print (f'  Number of sites: {len(sites)}')
        for s in sites:
            print (f"    {s['netcode']} {s['lookupcode']} ({s['ondate']} - {s['offdate']})")
            
        print (f'  Number of equipment installations: {len(equipinstalls)}')
        for eq in equipinstalls:
            print (f"    {eq['category']} {eq['modelname']} s/n {eq['serialnumber']} installed at {eq['netcode']} {eq['lookupcode']} on {eq['ondate']}")


    except Exception as e:
        logger.exception(e)

    finally:
        logger.info('Terminated')

if __name__ == '__main__':
    main()