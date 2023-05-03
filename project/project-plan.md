# Project Plan

## Summary
This projects aims to analyze how the weather influences the timetables of DB trains. Correlations (not necessarily causalities) are to be investigated, especially between train delays and bad weather. 


## Rationale
The analysis helps people who depend on punctual trains to understand whether the weather affects the punctuality of trains. This means, for example, that longer transfer times can be planned in advance if the weather forecast is poor.



## Datasources

### Datasource 1: Aktuelle stündliche Lufttemperatur und Luftfeuchte, gemessen an Stadtklimastationen, für ausgewählte urbane Räume in Deutschland by Bundesministerium für Digitales und Verkehr (BMDV) 
* Metadata URL: https://mobilithek.info/offers/-3781580859517637464
* Data URL:  https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate_urban/hourly/air_temperature/recent/ 
* Data Type: ZIP (txt and xlsx)

The Data describes climate data containing station, air temperature and humidity.

### Datasource 2: Timetables 1.0.213 by DB Station&Service AG
* Metadata URL: https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables/api/26494#/Timetables_10213/overview
* Metadata URL: https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1
* Data Type: REST API

This is a REST API for passenger information for train stations operated by DB Station&Service AG. There are attributes like the station, the timetable or the delay available.

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
