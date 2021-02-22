[![capital-region-vaccine-check](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml/badge.svg)](https://github.com/CapitalRegionVaccine/CapitalRegionVaccine/actions/workflows/sites-check.yml)

# Capital Region Covid 19 Vaccine Checker

This repository checks several locations in the New York State Capital Region for availability of Covid 19 vaccination appointments.

<!--start: status pages-->
**Last Updated**: 2021-02-22 08:19 AM

| Site                | Status         |
| ------------------- | -------------- |
| [Suny Albany](https://am-i-eligible.covid19vaccine.health.ny.gov/)         | :no_entry: Unavailable    |
| [Price Chopper](https://www.pricechopper.com/covidvaccine/new-york/)       | :white_check_mark: Available      |
| [CVS](https://www.cvs.com/immunizations/covid-19-vaccine)                 | :no_entry: Unavailable    |
| [Walgreens](https://www.walgreens.com/findcare/vaccination/covid-19/location-screening)           | :no_entry: Unavailable    |
<!--end: status pages-->

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

## Historical data

Historical availability data from previous checks can be found in the [data/site-data.csv](data/site-data.csv) spreadsheet.

## 📄 License

- Code: [MIT](./LICENSE)
