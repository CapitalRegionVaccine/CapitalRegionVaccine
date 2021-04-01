#!/usr/bin/env python3
import requests
import json
import pandas as pd
import tweepy
import os
import config as cfg
import time
import asyncio
import aiohttp
from time import sleep
from datetime import datetime, timedelta
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from geopy.distance import geodesic

def main():
    # get data
    tz = timezone('America/New_York')
    print( "-- starting nys_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    nys_data = get_nys_data()
    nys = get_nys_appt(nys_data, cfg.config["nys_sites"])
    alb = get_nys_appt(nys_data, cfg.config["alb_sites"])
    qns = get_nys_appt(nys_data, cfg.config["qns_sites"])
    print( "-/ ending nys_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    cvs = get_cvs_data()
    print( "-/ ending cvs_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    pc  = get_pc_data()
    print( "-/ ending pc_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    wal = get_walgreens_data()
    print( "-/ ending wal_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    wmt = get_walmart_data()
    print( "-/ ending wmt_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    han = get_han_data()
    print( "-/ ending han_data " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )
    #tuc = get_tuc_data()
    tuc = "Unavailable"

    # book urls
    nys_url = 'https://am-i-eligible.covid19vaccine.health.ny.gov/'
    cvs_url = 'https://www.cvs.com/immunizations/covid-19-vaccine'
    wal_url = 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    pc_url = 'https://www.pricechopper.com/covidvaccine/new-york/'
    han_url = 'https://www.hannaford.com/pharmacy/covid-19-vaccine'
    tuc_url = 'https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F'
    wmt_url = 'https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes'

    # img urls
    nys_img = '<img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13">'
    cvs_img = '<img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13">'
    wal_img = '<img alt="" src="https://favicons.githubusercontent.com/www.walgreens.com" height="13">'
    pc_img = '<img alt="" src="https://favicons.githubusercontent.com/www.pricechopper.com" height="13">'
    han_img = '<img alt="" src="https://favicons.githubusercontent.com/www.hannaford.com" height="13">'
    wmt_img = '<img alt="" src="https://favicons.githubusercontent.com/www.walmart.com" height="13">'

    date = str(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
    sites = ['SUNY Albany','Albany Armory','Queensbury Mall','Price Chopper','CVS','Walgreens','Hannaford','Times Union Center','Walmart']
    appointments = [ nys, alb, qns, pc, cvs, wal, han, tuc, wmt ]
    df_long = pd.DataFrame({'date': date, 'appointments': appointments, 'sites': sites})
    df_long.head()

    # wide format
    df_wide = df_long.pivot(index = 'date', columns = 'sites', values = 'appointments').reset_index()
    df_wide.head()

    try:
        df_historical = pd.read_csv('data/site-data.csv')

        ##Pull data from last row of history
        last_data = df_historical.iloc[0]

        ##Maybe tweet new availability
        if nys.startswith( 'Available' ) and not last_data['SUNY Albany'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at SUNY Albany. ' + nys_url)
        if cvs.startswith( 'Available' ) and not last_data['CVS'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at CVS. ' + cvs[9:] + " " + cvs_url)
        if wal.startswith( 'Available' ) and not last_data['Walgreens'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Walgreens. ' + wal[9:] + wal_url)
        if pc.startswith( 'Available' ) and not last_data['Price Chopper'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Price Chopper. ' + pc[9:] + " " + pc_url)
        if alb.startswith( 'Available' ) and not ( last_data['Albany Armory'].startswith( 'Available' ) or last_data['Albany Armory'].startswith( 'ERROR' ) ):
            tweet_it('Vaccination appointments are available at Albany Armory (**resident restricted). ' + nys_url)
        if han.startswith( 'Available' ) and not last_data['Hannaford'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Hannaford ' + han[9:] + han_url)
        if tuc.startswith( 'Available' ) and not last_data['Times Union Center'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Times Union Center '+ tuc_url)
        if wmt.startswith( 'Available' ) and not last_data['Walmart'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Walmart ' + wmt[9:] + wmt_url)
        if qns.startswith( 'Available' ) and not last_data['Queensbury Mall'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Queensbury Mall. ' + nys_url)

        ##Maybe tweet new unavailability
        if "Unavailable" == nys and last_data['SUNY Albany'].startswith( 'Available' ):
            tweet_it('SUNY Albany vaccination appointments are now closed.')
        if "Unavailable" == cvs and last_data['CVS'].startswith( 'Available' ):
            tweet_it('CVS vaccination appointments are now closed.')
        if "Unavailable" == wal and last_data['Walgreens'].startswith( 'Available' ):
            tweet_it('Walgreens vaccination appointments are now closed.')
        if "Unavailable" == pc and last_data['Price Chopper'].startswith( 'Available' ):
            tweet_it('Price Chopper vaccination appointments are now closed.')
        if "Unavailable" == alb and last_data['Albany Armory'].startswith( 'Available' ):
            tweet_it('Albany Armory vaccination appointments are now closed.')
        if "Unavailable" == han and last_data['Hannaford'].startswith( 'Available' ):
            tweet_it('Hannaford vaccination appointments are now closed.')
        if "Unavailable" == tuc and last_data['Times Union Center'].startswith( 'Available' ):
            tweet_it('Times Union Center vaccination appointments are now closed.')
        if "Unavailable" == wmt and last_data['Walmart'].startswith( 'Available' ):
            tweet_it('Walmart vaccination appointments are now closed.')
        if "Unavailable" == qns and last_data['Queensbury Mall'].startswith( 'Available' ):
            tweet_it('Queensbury Mall vaccination appointments are now closed.')

    except pd.errors.EmptyDataError:
        df_historical = pd.DataFrame()


    # append today's data 
    df_historical = df_historical.append(df_wide).sort_values(by = 'date', ascending = False)

    # save updated file 
    df_historical.to_csv('data/site-data.csv', index = False)
    print( "-/ ending csv write " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )

    md_file = open('README.md', 'r')
    new_md_content = ''
    start_rpl = False
    for line in md_file:
        stripped_line = line.rstrip('\r\n')
        if '<!--end: status pages-->' == stripped_line:
            start_rpl = False
            new_md_content += "**Last Updated**: " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M %p')) + "\n\n"
            new_md_content += "| Site                | Status         |\n"
            new_md_content += "| ------------------- | -------------- |\n"
            new_md_content += "| " + nys_img + " [Suny Albany](" + nys_url + ")      | " + stat_check(nys) + "    |\n"
            new_md_content += "| " + nys_img + " [Albany Armory](" + nys_url + ")    | " + stat_check(alb) + "    |\n"
            new_md_content += "| " + nys_img + " [Queensbury Mall](" + nys_url + ")    | " + stat_check(qns) + "    |\n"
            new_md_content += "| " + nys_img + " [Times Union Center](" + tuc_url + ")| " + stat_check(tuc) + "    |\n"
            new_md_content += "| " + pc_img + " [Price Chopper](" + pc_url + ")     | " + stat_check(pc) + "    |\n"
            new_md_content += "| " + cvs_img + " [CVS](" + cvs_url + ")               | " + stat_check(cvs) + "    |\n"
            new_md_content += "| " + wal_img + " [Walgreens](" + wal_url + ")         | " + stat_check(wal) + "    |\n"
            new_md_content += "| " + han_img + " [Hannaford](" + han_url + ")         | " + stat_check(han) + "    |\n"
            new_md_content += "| " + wmt_img + " [Walmart](" + wmt_url + ")         | " + stat_check(wmt) + "    |\n"


        if start_rpl != True:
            new_md_content += stripped_line + "\n"
        if '<!--start: status pages-->' == stripped_line:
            start_rpl = True

    md_file.close()

    md_file = open('README.md', 'w')
    md_file.write(new_md_content)
    md_file.close()
    print( "-/ finished " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S %p')) )


def stat_check(data):
    if data.startswith( 'Available' ):
        data = ':white_check_mark: ' + data + '  '
    else:
        data = ':no_entry: ' + data
    return data

def get_nys_data():
    headers = {'referer': 'https://am-i-eligible.covid19vaccine.health.ny.gov/'}
    try:
        req = requests.get('https://am-i-eligible.covid19vaccine.health.ny.gov/api/list-providers', headers=headers)
    except requests.exceptions.RequestException as e:
        return "ERROR"

    try:
        json_object = json.loads(req.text)
    except ValueError as e:
        return "ERROR"

    json_response = req.json()
    return json_response

def get_nys_appt(json_response, nys_sites):
    if "ERROR" == json_response:
        return json_response
    
    if "providerList" not in json_response:
        return "ERROR"

    is_available = ''
    for provider in json_response['providerList']:
        if provider['providerName'] in nys_sites:
            if "Y" == provider['availableAppointments']:
                is_available = is_available + provider['providerName'] + " "
    
    if len(is_available) > 0:
        return "Available" + is_available
    else:
        return "Unavailable"

def get_han_data():
    results = asyncio.get_event_loop().run_until_complete(run_hannaford_data())
    return results

async def run_hannaford_data():
    async with aiohttp.ClientSession() as session:
        await session.get('https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory')
        tasks = [asyncio.create_task(get_hannaford_site_information(site, session)) for site in cfg.config["han_sites"]]
        results = await asyncio.gather(*tasks)
        sites = ''
        for site in results:
            if site != '' and site != "ERROR":
                sites = sites + ' ' + site
        if len(sites) > 0:
            return "Available" + sites
        else:
            return "Unavailable"

async def get_hannaford_site_information(site,session):
    tz = timezone('America/New_York')
    url = 'https://hannafordsched.rxtouch.com/rbssched/program/covid19/Calendar/PatientCalendar'
    year = str(datetime.now(tz).strftime('%Y'))
    month =  datetime.now(tz).strftime('X%m').replace('X0','X').replace('X','')
    data = {
        'facilityId': site,
        'month': month,
        'year': year,
        'snapCalendarToFirstAvailMonth': 'false'
    }

    try:
        async with session.post(url,data=data) as response:
            if response.status == 200:
                try: 
                    text = await response.text()
                    json_object = json.loads(text)
                except ValueError as e:
                    return "ERROR"

                json_response = await response.json()
            else:
                return "ERROR"
    except aiohttp.ClientConnectorError as e:
        return "ERROR"

    site_avail = False
    if 'Data' in json_response:
        if 'Days' in json_response['Data']:
            for day in json_response['Data']['Days']:
                if True == day['Available']:
                    site_avail = True

    is_available = ''
    if site_avail == True:
        is_available = cfg.config["han_sites"][site]

    return is_available

def get_pc_data():
    try:
        req = requests.get('https://scrcxp.pdhi.com/ScreeningEvent/e047c75c-a431-41a8-8383-81613f39dd55/GetLocations/' + cfg.config["zipcode"] + '?state=NY')
    except requests.exceptions.RequestException as e:
        return "ERROR"
    json_response = req.json()

    if len(json_response) > 0:
        is_available = ''
        for response in json_response:
            city = response['city']
            slots = 0

            for timeslot in response['timeSlots']:
                if True != timeslot['isFull']:
                    slots += 1

            if slots > 0:
                is_available = is_available + " " + city + '(' + str(slots) + ')'

        if len(is_available) > 0:
            return "Available" + is_available
        else:
            return "Unavailable"
    else:
        return "Unavailable"

def get_cvs_data():
    headers = {'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine'}
    try:
        req = requests.get('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.NY.json?vaccineinfo', headers=headers)
    except requests.exceptions.RequestException as e:
        return "ERROR"

    json_response = req.json()
    if 'responsePayloadData' not in json_response:
        return "ERROR"
    else:
        if 'data' not in json_response['responsePayloadData']:
            return "ERROR"
        else:
            if 'NY' not in json_response['responsePayloadData']['data']:
                return "ERROR"

    message = ''
    for provider in json_response['responsePayloadData']['data']['NY']:
        city = provider['city']
        status = provider['status']
        total = 0
        if 'totalAvailable' in provider:
            total = provider['totalAvailable']
        if city in cfg.config["cvs_sites"] and status != 'Fully Booked':
            message = message + city.title() + ' '
    if message != "":
        return "Available " + message
    else:
        return "Unavailable"

def get_walmart_data():
    url = 'https://www.vaccinespotter.org/api/v0/stores/NY/walmart.json'
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "ERROR"
    json_response = req.json()

    latham = (42.744869, -73.752037)

    message = ''
    for site in json_response:
        site_long = (site['latitude'], site['longitude'])
        distance = geodesic(latham, site_long).miles
        if distance < 30:
            if site['appointments_available'] == True:
                message = message + site['city'] + ' (' + str(len(site['appointments'])) + ') '

    if message != "":
        return "Available " + message
    else:
        return "Unavailable"

def get_walgreens_data():
    url = 'https://www.vaccinespotter.org/api/v0/stores/NY/walgreens.json'
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "ERROR"
    json_response = req.json()

    latham = (42.744869, -73.752037)

    message = ''
    for site in json_response:
        site_long = (site['latitude'], site['longitude'])
        distance = geodesic(latham, site_long).miles
        if distance < 25:
            if site['appointments_available'] == True:
                count = 0
                for appointment in site['appointments']:
                    if 'type' in appointment:
                        if "2nd Dose Only" not in appointment['type']:
                            count = count + 1

                message = message + site['city'].title() + ' (' + str(count) + ') '

    if message != "":
        return "Available " + message
    else:
        return "Unavailable"

def get_tuc_data():
    is_available = "Unavailable"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    chromedriver_path = os.environ.get('CHROMEWEBDRIVER', './chromedriver.exe')
    print(f'Using chromedriver: {chromedriver_path}')
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.headless = True
    
    url = 'https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F'

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ny-universal-footer"]')))
    except TimeoutException:
        driver.close()
        driver.quit()
        print("TIMEOUT waiting")
        return "ERROR"

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    appointments = soup.select("div[class='col-sm-11 col-md-10 col-lg-11 col-xl-11']")

    if appointments is not None:
        if len(appointments) > 0:
            is_available = "Available"

    driver.close()
    driver.quit()
    return is_available

def tweet_it(message):
    CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    ACCESS_KEY = os.environ.get('TWITTER_ACCESS_KEY')
    ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    ##TODO: Error handling
    ##Try to get around twitter duplicate messaging
    tz = timezone('America/New_York')
    message = message + " [" + str(datetime.now(tz).strftime('%m-%d-%Y %I:%M %p')) + "]"
    print("Tweeting message: " + message)
    api.update_status(message)


main()
