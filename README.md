# web-data-scraping

<img src="https://i0.wp.com/ledatascientist.com/wp-content/uploads/2020/10/scrapy_big.png" height="100" />
This is a project to try online data scraping with Scrapy.

### Script n°1 - Apple mobility data

Script : `covid19_mobility_data_scraping.py`

All datas are available here : [covid19.apple.com/mobility](https://covid19.apple.com/mobility)

This script scrapes a csv data file from the link, converts the data into a Pandas dataframe.


### Script n°2 - Crop FSA data

Script : `crop_data_scraping.py`

All datas are available here : [fsa.usda.gov](https://www.fsa.usda.gov/news-room/efoia/electronic-reading-room/frequently-requested-information/crop-acreage-data/index)

This script takes a list of years as argument.
For each year, the data are extracted from the website, saved into a `.zip` file and extracted in the `data/` folder.
The `country_data` Excel sheet is extracted for each year and converted into a dataframe with the publication date.
