# Project Plan

## Summary
This projects aims to analyze how the weather influences the timetables of DB trains. Correlations (not necessarily causalities) are to be investigated, especially between train delays and bad weather. 


## Rationale
The analysis helps people who depend on punctual trains to understand whether the weather affects the punctuality of trains. This means, for example, that longer transfer times can be planned in advance if the weather forecast is poor.



## Datasources

### Datasource 1: Fahrplan API (Timetables 1.0.213) by DB Station&Service AG
* Metadata URL: https://mobilithek.info/offers/-3916716856299319220
* Data URL: https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1
* Data Overview: https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables/api/26494#/Timetables_10213/overview
* Data Type: xml by REST API

This is a REST API for passenger information for train stations operated by DB Station&Service AG. There are attributes like the station, the timetable or the delay available.

To access the data, it is necessary to create a BahnID account. After subscribing to the API, you will receive the API key. You are allowed to use the data under the license Creative Commons Attribution 4.0 International (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/. 

The station IDs required for querying the timetables can be accessed by https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/*


### Datasource 2: Historical weather and climate data by Meteostat Developers
* Metadata URL: https://dev.meteostat.net/
* Data URL:  https://bulk.meteostat.net/v2 
* Data Type: zipped csv with bulk data interface which provides full data dumps 

The endpoint provides a zipped CSV file for weather stations hourly, daily or monthly. The data contains data such as air temperature, precipitation or sunshine minutes.

The weather station IDs that have sent data in the past can be looked up at the endpoint https://bulk.meteostat.net/v2/stations/lite.json.gz

## Work Packages
1. Automated data pipeline [#1][i1]
2. Automated tests [#2][i2]
3. Continuos integration [#3][i3]
4. Data Exploration [#4][i4]
5. Data Analysis [#5][i5]
6. Deployment on GitHub [#6][i6]

[i1]: https://github.com/janinepa/2023-amse-template/issues/1
[i2]: https://github.com/janinepa/2023-amse-template/issues/2
[i3]: https://github.com/janinepa/2023-amse-template/issues/3
[i4]: https://github.com/janinepa/2023-amse-template/issues/4
[i5]: https://github.com/janinepa/2023-amse-template/issues/5
[i6]: https://github.com/janinepa/2023-amse-template/issues/6
