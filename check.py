#!/usr/bin/env python3
import requests
import json
import pandas as pd
import tweepy
import os
import config as cfg
import time
from datetime import datetime, timedelta
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    # get data
    nys_data = get_nys_data()
    nys = get_nys_appt(nys_data, cfg.config["nys_sites"])
    alb = get_nys_appt(nys_data, cfg.config["alb_sites"])
    cvs = get_cvs_data()
    pc  = get_pc_data()
    wal = get_walgreens_data()
    han = get_han_data()
    tuc = get_tuc_data()

    # book urls
    nys_url = 'https://am-i-eligible.covid19vaccine.health.ny.gov/'
    cvs_url = 'https://www.cvs.com/immunizations/covid-19-vaccine'
    wal_url = 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    pc_url = 'https://www.pricechopper.com/covidvaccine/new-york/'
    han_url = 'https://www.hannaford.com/pharmacy/covid-19-vaccine'
    tuc_url = 'https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F'

    # img urls
    nys_img = '<img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13">'
    cvs_img = '<img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13">'
    wal_img = '<img alt="" src="https://favicons.githubusercontent.com/www.walgreens.com" height="13">'
    pc_img = '<img alt="" src="https://favicons.githubusercontent.com/www.pricechopper.com" height="13">'
    han_img = '<img alt="" src="https://favicons.githubusercontent.com/www.hannaford.com" height="13">'

    tz = timezone('EST')
    date = str(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
    sites = ['SUNY Albany','Albany Armory','Price Chopper','CVS','Walgreens','Hannaford','Times Union Center']
    appointments = [ nys, alb, pc, cvs, wal, han, tuc ]
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
            tweet_it('Vaccination appointments are available at Walgreens. ' + wal_url)
        if pc.startswith( 'Available' ) and not last_data['Price Chopper'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Price Chopper. ' + pc[9:] + " " + pc_url)
        if alb.startswith( 'Available' ) and not last_data['Albany Armory'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Albany Armory (**resident restricted). ' + nys_url)
        if han.startswith( 'Available' ) and not last_data['Hannaford'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Hannaford ' + han[9:] + han_url)
        if tuc.startswith( 'Available' ) and not last_data['Times Union Center'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at Times Union Center '+ tuc_url)

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
        stripped_line = line.rstrip('\r\n')
        if '<!--end: status pages-->' == stripped_line:
            start_rpl = False
            new_md_content += "**Last Updated**: " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M %p')) + "\n\n"
            new_md_content += "| Site                | Status         |\n"
            new_md_content += "| ------------------- | -------------- |\n"
            new_md_content += "| " + nys_img + " [Suny Albany](" + nys_url + ")      | " + stat_check(nys) + "    |\n"
            new_md_content += "| " + nys_img + " [Albany Armory](" + nys_url + ")    | " + stat_check(alb) + "    |\n"
            new_md_content += "| " + nys_img + " [Times Union Center](" + tuc_url + ")| " + stat_check(tuc) + "    |\n"
            new_md_content += "| " + pc_img + " [Price Chopper](" + pc_url + ")     | " + stat_check(pc) + "    |\n"
            new_md_content += "| " + cvs_img + " [CVS](" + cvs_url + ")               | " + stat_check(cvs) + "    |\n"
            new_md_content += "| " + wal_img + " [Walgreens](" + wal_url + ")         | " + stat_check(wal) + "    |\n"
            new_md_content += "| " + han_img + " [Hannaford](" + han_url + ")         | " + stat_check(han) + "    |\n"

        if start_rpl != True:
            new_md_content += stripped_line + "\n"
        if '<!--start: status pages-->' == stripped_line:
            start_rpl = True

    md_file.close()

    md_file = open('README.md', 'w')
    md_file.write(new_md_content)
    md_file.close()

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
            if "NAC" != provider['availableAppointments']:
                is_available = is_available + provider['providerName'] + " "
    
    if len(is_available) > 0:
        return "Available" + is_available
    else:
        return "Unavailable"

def get_han_data():
    session = requests.session()
    try:
        session.get('https://hannafordsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory')
    except requests.exceptions.RequestException as e:
        return "ERROR"

    url = ' https://hannafordsched.rxtouch.com/rbssched/program/covid19/Calendar/PatientCalendar'
    tz = timezone('EST')
    year = str(datetime.now(tz).strftime('%Y'))
    month =  datetime.now(tz).strftime('X%m').replace('X0','X').replace('X','')

    is_available = ''
    for site in cfg.config["han_sites"]:
        data = {
            'facilityId': site,
            'month': month,
            'year': year,
            'snapCalendarToFirstAvailMonth': 'false'
        }

        try:
            req = session.post(url, data=data)
        except requests.exceptions.RequestException as e:
            return "ERROR"

        try:
            json_object = json.loads(req.text)
        except ValueError as e:
            print("Hannaford json error")
            return "ERROR"

        json_response = req.json()
        if 'Data' in json_response:
            if 'Days' in json_response['Data']:
                for day in json_response['Data']['Days']:
                    if True == day['Available']:
                        is_available = ' (' +  str(day['DayOfWeek']) + ' ' + str(day['DayNumber']) + ')'

    if len(is_available) > 0:
        return "Available" + is_available
    else:
        return "Unavailable"

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
            message = message + city + ' '
    if message != "":
        return "Available " + message
    else:
        return "Unavailable"

def get_walgreens_data():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    chromedriver_path = os.environ.get('CHROMEWEBDRIVER', './chromedriver.exe')
    print(f'Using chromedriver: {chromedriver_path}')
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("window-size=1280,800")
    options.headless = True

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.get('https://www.walgreens.com')

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wag-footer-disclaimer-new"]')))
    except TimeoutException:
        driver.close
        driver.quit
        print("TIMEOUT waiting 1")
        return "ERROR"


    url = 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inputLocation"]')))
    except TimeoutException:
        driver.close
        driver.quit
        print("TIMEOUT waiting 2")
        return "ERROR"

    locationInput = driver.find_element_by_id("inputLocation")
    locationInput.click()
    locationInput.clear()
    locationInput.send_keys(cfg.config["zipcode"])
    time.sleep(1)
    driver.find_element_by_class_name("btn").click()

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//p[contains(@class, "fs16")]')))
    except TimeoutException:
        driver.close
        driver.quit
        print("TIMEOUT waiting 3")
        return "ERROR"


    popUp = driver.find_element_by_class_name("fs16")
    if popUp.text != "Appointments unavailable":
        driver.close
        driver.quit
        return "Available"
    else:
        driver.close
        driver.quit
        return "Unavailable"


def get_walgreens_datax():
    session = requests.session()
    try:
        print("Getting walgreens start")
        session.get('https://www.walgreens.com/findcare/vaccination/covid-19/location-screening', timeout=20)
    except requests.exceptions.RequestException as e:
        print("WG timeout")
        return "ERROR"

    url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability'
    date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    headers = {
        'referer': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening',
        'content-type': 'application/json; charset=UTF-8',
    }
    body = '{"serviceId":"99","position":{' + cfg.config["wal_location"] + '},"appointmentAvailability":{"startDateTime":"' + date + '"},"radius":25}'
    try:
        print("Getting walgreens next")
        req = session.post(url, data=body, headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:
        return "ERROR"
    
    json_response = req.json()
    if 'appointmentsAvailable' not in json_response:
        return "ERROR"

    if False == json_response['appointmentsAvailable']:
        return "Unavailable"
    else:
        return "Available"

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
        driver.close
        driver.quit
        print("TIMEOUT waiting")
        return "ERROR"

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    appointments = soup.select("div[class='col-sm-11 col-md-10 col-lg-11 col-xl-11']")

    if appointments is not None:
        if len(appointments) > 0:
            is_available = "Available"

    driver.close
    driver.quit
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
    tz = timezone('EST')
    message = message + " [" + str(datetime.now(tz).strftime('%m-%d-%Y %I:%M %p')) + "]"
    print("Tweeting message: " + message)
    api.update_status(message)


main()