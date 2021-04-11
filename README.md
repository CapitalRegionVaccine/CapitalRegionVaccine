[![capital-region-vaccine-check](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml/badge.svg)](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml)

# Capital Region Covid 19 Vaccine Checker

This repository checks several locations in the New York State Capital Region for availability of Covid 19 vaccination appointments.

Follow our <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> **[Twitter bot](https://twitter.com/RegionVaccine)** <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> to get notified of new appointment availability!

<!--start: status pages-->
**Last Updated**: 2021-04-10 10:20 PM

| Site                | Status         |
| ------------------- | -------------- |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Suny Albany](https://am-i-eligible.covid19vaccine.health.ny.gov/)      | :white_check_mark: AvailableSUNY Albany       |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Albany Armory](https://am-i-eligible.covid19vaccine.health.ny.gov/)    | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Queensbury Mall](https://am-i-eligible.covid19vaccine.health.ny.gov/)    | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Times Union Center](https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F)| :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.pricechopper.com" height="13"> [Price Chopper](https://www.pricechopper.com/covidvaccine/new-york/)     | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13"> [CVS](https://www.cvs.com/immunizations/covid-19-vaccine)               | :white_check_mark: Available Albany Colonie Queensbury Schenectady Troy Wynantskill       |
| <img alt="" src="https://favicons.githubusercontent.com/www.walgreens.com" height="13"> [Walgreens](https://www.walgreens.com/findcare/vaccination/covid-19/location-screening)         | :white_check_mark: Available Saratoga Springs (0) Schenectady (0) Schenectady (105) Colonie (0) Albany (0) Rotterdam (54)       |
| <img alt="" src="https://favicons.githubusercontent.com/www.hannaford.com" height="13"> [Hannaford](https://www.hannaford.com/pharmacy/covid-19-vaccine)         | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.walmart.com" height="13"> [Walmart](https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes)         | :white_check_mark: Available East Greenbush (26) Glenmont (36) Latham (33) Clifton Park (25) Schenectady (17) Saratoga Springs (60)       |
<!--end: status pages-->

## Other locations

Here are a few other places to check we do not have automated checks setup for:

* [Capital Region RX](https://capitalregionalrx.com/covid-vaccine-appointment/)
* [WellNow - Latham](https://www.clockwisemd.com/hospitals/5761/appointments/schedule_visit)
* [WellNow - Clifton Park](https://www.clockwisemd.com/hospitals/4409/appointments/schedule_visit)
* [WellNow - Saratoga](https://www.clockwisemd.com/hospitals/6471/appointments/schedule_visit)

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
