[![capital-region-vaccine-check](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml/badge.svg)](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml)

# Capital Region Covid 19 Vaccine Checker

This repository checks several locations in the New York State Capital Region for availability of Covid 19 vaccination appointments.

Follow our <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> **[Twitter bot](https://twitter.com/RegionVaccine)** <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> to get notified of new appointment availability!

<!--start: status pages-->
**Last Updated**: 2021-03-23 02:40 AM

| Site                | Status         |
| ------------------- | -------------- |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Suny Albany](https://am-i-eligible.covid19vaccine.health.ny.gov/)      | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Albany Armory](https://am-i-eligible.covid19vaccine.health.ny.gov/)    | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Queensbury Mall](https://am-i-eligible.covid19vaccine.health.ny.gov/)    | :white_check_mark: AvailableQueensbury Aviation Mall - Sears       |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Times Union Center](https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F)| :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.pricechopper.com" height="13"> [Price Chopper](https://www.pricechopper.com/covidvaccine/new-york/)     | :white_check_mark: Available Latham(3) Albany(9) Albany(10) Troy(10) Guilderland(6) Clifton Park(1) Glenmont(10) Renselaer(9)      |
| <img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13"> [CVS](https://www.cvs.com/immunizations/covid-19-vaccine)               | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.walgreens.com" height="13"> [Walgreens](https://www.walgreens.com/findcare/vaccination/covid-19/location-screening)         | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.hannaford.com" height="13"> [Hannaford](https://www.hannaford.com/pharmacy/covid-19-vaccine)         | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.walmart.com" height="13"> [Walmart](https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes)         | :no_entry: Unavailable    |
<!--end: status pages-->

\*\* *Albany Armory is currently restricted to certain residents.  Please check the NYS website for more details.*  
\*\*\* *Pharmacies are currently restricted to those 60 and older in NYS and those with comorbidities.  Please check each for individual restrctions.*

## Site Information

This checks the following locations approximatly every 5 minutes using GitHub Actions.

* SUNY Albany NYS Vaccination Site
* Queensbury Mall NYS Vaccination Site
* Price Chopper Capital Region locations
* Walgreens within a 25 mile radius of 12110 (Latham, NY)
* The following CVS locations:
  * Wynantskill
  * Saratoga Springs
  * Colonie
  * Glenville
  * Queensbury
  * Albany
  * Troy
  * Glenville
  * Latham
  * Rensselaer
  * Schenectady
* The following Hannaford locations:
  * Albany
  * Ballston Lake
  * Voorheesville
  * Wynantskill
  * Altamont
  * Ballston Spa
  * Clifton Park
  * Niskayuna
  * Saratoga Springs
  * Latham
  * Troy
  * Valatie
  * Saratoga Springs
  * Amsterdam
* Walmart locations within 30 miles of Latham, NY

## Historical data

Historical availability data from previous checks can be found in the [data/site-data.csv](data/site-data.csv) spreadsheet.

## 📄 License

- Code: [MIT](./LICENSE)
