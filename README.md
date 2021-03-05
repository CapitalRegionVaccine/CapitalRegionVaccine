[![capital-region-vaccine-check](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml/badge.svg)](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml)

# Capital Region Covid 19 Vaccine Checker

This repository checks several locations in the New York State Capital Region for availability of Covid 19 vaccination appointments.

Follow our <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> **[Twitter bot](https://twitter.com/RegionVaccine)** <img alt="" src="https://favicons.githubusercontent.com/www.twitter.com" height="13"> to get notified of new appointment availability!

<!--start: status pages-->
**Last Updated**: 2021-03-04 09:10 PM

| Site                | Status         |
| ------------------- | -------------- |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Suny Albany](https://am-i-eligible.covid19vaccine.health.ny.gov/)      | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Albany Armory](https://am-i-eligible.covid19vaccine.health.ny.gov/)    | :white_check_mark: Available**Washington Avenue Armory - Albany, Schenectady, Troy       |
| <img alt="" src="https://favicons.githubusercontent.com/am-i-eligible.covid19vaccine.health.ny.gov" height="13"> [Times Union Center](https://apps2.health.ny.gov/doh2/applinks/cdmspr/2/counties?DateID=BBF046E734D3128CE0530A6C7C165A0F)| :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.pricechopper.com" height="13"> [Price Chopper](https://www.pricechopper.com/covidvaccine/new-york/)     | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13"> [CVS](https://www.cvs.com/immunizations/covid-19-vaccine)               | :white_check_mark: Available COLONIE GLENVILLE QUEENSBURY SARATOGA SPRINGS WYNANTSKILL       |
| <img alt="" src="https://favicons.githubusercontent.com/www.walgreens.com" height="13"> [Walgreens](https://www.walgreens.com/findcare/vaccination/covid-19/location-screening)         | :no_entry: Unavailable    |
| <img alt="" src="https://favicons.githubusercontent.com/www.hannaford.com" height="13"> [Hannaford](https://www.hannaford.com/pharmacy/covid-19-vaccine)         | :white_check_mark: Available (Monday 8)      |
<!--end: status pages-->

\*\* *Albany Armory is currently restricted to certain residents.  Please check the NYS website for more details.*  
\*\*\* *Pharmacies are currently restricted to those 65 and older in NYS.  Please check each for individual restrctions.*

## Site Information

This checks the following locations approximatly every 5 minutes using GitHub Actions.

* SUNY Albany NYS Vaccination Site
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
* The following Hannaford locations:
  * Albany
  * Ballston Lake
  * Voorheesville

## Historical data

Historical availability data from previous checks can be found in the [data/site-data.csv](data/site-data.csv) spreadsheet.

## 📄 License

- Code: [MIT](./LICENSE)
