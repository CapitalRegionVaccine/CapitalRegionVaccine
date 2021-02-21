#!/usr/bin/env python3
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone

def main():
    # get data
    nys = get_nys_data()
    cvs = get_cvs_data()
    pc  = get_pc_data()
    wal = get_walgreens_data()

    # book urls
    nys_url = 'https://am-i-eligible.covid19vaccine.health.ny.gov/'
    cvs_url = 'https://www.cvs.com/immunizations/covid-19-vaccine'
    wal_url = 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    pc_url = 'https://www.pricechopper.com/covidvaccine/new-york/'
    
    tz = timezone('EST')
    date = str(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
    sites = ['SUNY Albany','Price Chopper','CVS','Walgreens']
    appointments = [ nys, pc, cvs, wal ]
    df_long = pd.DataFrame({'date': date, 'appointments': appointments, 'sites': sites})
    df_long.head()

    # wide format
    df_wide = df_long.pivot(index = 'date', columns = 'sites', values = 'appointments').reset_index()
    df_wide.head()

    try:
        df_historical = pd.read_csv('data/site-data.csv')
    except pd.errors.EmptyDataError:
        df_historical = pd.DataFrame()

    # append today's data 
    df_historical = df_historical.append(df_wide).sort_values(by = 'date', ascending = False)

    # save updated file 
    df_historical.to_csv('data/site-data.csv', index = False)

    md_file = open('README.md', 'r')
    new_md_content = ''
    start_rpl = False
    for line in md_file:
        stripped_line = line.strip()
        if '<!--end: status pages-->' == stripped_line:
            start_rpl = False
            new_md_content += "**Last Updated**: " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M %p')) + "\n\n"
            new_md_content += "| Site                | Status         |\n"
            new_md_content += "| ------------------- | -------------- |\n"
            new_md_content += "| [Suny Albany](" + nys_url + ")         | " + stat_check(nys) + "    |\n"
            new_md_content += "| [Price Chopper](" + pc_url + ")       | " + stat_check(pc) + "    |\n"
            new_md_content += "| [CVS](" + cvs_url + ")                 | " + stat_check(cvs) + "    |\n"
            new_md_content += "| [Walgreens](" + wal_url + ")           | " + stat_check(wal) + "    |\n"

        if start_rpl != True:
            new_md_content += stripped_line + "\n"
        if '<!--start: status pages-->' == stripped_line:
            start_rpl = True

    md_file.close()

    md_file = open('README.md', 'w')
    md_file.write(new_md_content)
    md_file.close()

def stat_check(data):
    if 'Available' == data:
        data = ':white_check_mark: ' + data + '  '
    else:
        data = ':no_entry: ' + data
    return data

def get_nys_data():
    headers = {'referer': 'https://am-i-eligible.covid19vaccine.health.ny.gov/'}
    req = requests.get('https://am-i-eligible.covid19vaccine.health.ny.gov/api/list-providers', headers=headers)
    json_response = req.json()
    for provider in json_response['providerList']:
        if "SUNY Albany " == provider['providerName']:
            if "NAC" != provider['availableAppointments']:
                return "Available"
            else:
                return "Unavailable"
    
    return "ERROR"

def get_pc_data():
    req = requests.get('https://scrcxp.pdhi.com/ScreeningEvent/e047c75c-a431-41a8-8383-81613f39dd55/GetLocations/12065?state=NY')
    json_response = req.json()
    if len(json_response) > 0:
        return "Available"
    else:
        return "Unavailable"

def get_cvs_data():
    headers = {'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine'}
    req = requests.get('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.NY.json?vaccineinfo', headers=headers)
    json_response = req.json()
    message = ''
    for provider in json_response['responsePayloadData']['data']['NY']:
        city = provider['city']
        status = provider['status']
        total = provider['totalAvailable']
        if city in ['WYNANTSKILL', 'SARATOGA SPRINGS', 'COLONIE', 'GLENVILLE', 'QUEENSBURY'] and status != 'Fully Booked' and total > 0:
            message = message + "Available " + city + '(' + total + ')  '
    if message != "":
        return message
    else:
        return "Unavailable"

def get_walgreens_data():
    url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    headers = {
        'referer': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening',
        'content-type': 'application/json; charset=UTF-8',
    }
    body = '{"serviceId":"99","position":{"latitude":42.7477661,"longitude":-73.760537},"appointmentAvailability":{"startDateTime":"' + date + '"},"radius":25}'
    req = requests.post(url, data=body, headers=headers)
    json_response = req.json()
    if False == json_response['appointmentsAvailable']:
        return "Unavailable"
    else:
        return "Available"

main()