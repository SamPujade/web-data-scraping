# Source data :
# https://www.fsa.usda.gov/news-room/efoia/electronic-reading-room/frequently-requested-information/crop-acreage-data/index

# Point of the script:
# With a list of years as an input, extract every xlxs database from this year and use it as a pandas dataframe + add publication date

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.pipelines.files import FilesPipeline
import re
import os
import glob
from zipfile import ZipFile

def filter_hrefs(hrefs, years):
    hrefs_by_year, all_hrefs = {}, []
    for year in years:
        hrefs_by_year[year] = []

    for href in hrefs:
        year_match = re.match(r'.*([1-3][0-9]{3}-crop)', href)
        if year_match is not None:
            year = year_match.group(1)[:4]
            if year in years:
                hrefs_by_year[year].append({'link': href, 'publication_date': href[-10:-4]})
                all_hrefs.append(href)

    return hrefs_by_year, all_hrefs

class DownloadItems(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class CropsSpider(scrapy.Spider):
    name = "crops"
    start_urls = ["https://www.fsa.usda.gov/news-room/efoia/electronic-reading-room/frequently-requested-information/crop-acreage-data/index"]

    def __init__(self, years=[], **kwargs):
        super().__init__(**kwargs)
        self.years = years

    def parse(self, response):
        hrefs = ['https://www.fsa.usda.gov' + href for href in response.css("div.rxbodyfield li a::attr(href)").extract() if href[-3:] == 'zip']
        hrefs_by_year, all_hrefs = filter_hrefs(hrefs, self.years)

        result = DownloadItems()

        result['file_urls'] = all_hrefs
        yield result

def GetCropDatas(years):

    settings = Settings()

    settings.set('ITEM_PIPELINES', {'scrapy.pipelines.files.FilesPipeline': 1})
    settings.set('FILES_STORE', './data/')

    process = CrawlerProcess(settings)

    spider = CropsSpider

    process.crawl(spider, years)
    process.start()

if __name__ == "__main__":
    GetCropDatas(['2021'])
    files = glob.glob('./data/full/*.zip')
    for f in files:
        zf = ZipFile(f, mode='r')
        zf.extractall(path=os.path.dirname(f))
        zf.close()
        os.remove(f)

    data_files = glob.glob('./data/full/*.xlsx')
    dataframes = [pd.read_excel(file, sheet_name='county_data') for file in data_files]
    for i in range(len(dataframes)):
        publication_date = data_files[i][-11:-5]
        dataframes[i]['Publication Date'] = publication_date
    print("Dataframe :", dataframes[0])