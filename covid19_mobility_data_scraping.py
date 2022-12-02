# Source data :
# https://covid19.apple.com/mobility

# Point of the script : 
# download csv database from website and use it as a pandas dataframe

import pandas as pd
import glob
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class CsvItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    FILES_RESULT_FIELD = 'covid19-mobility-data.csv'

class CovidSpider(scrapy.Spider):
    name = "Covid-19 Spider"

    def __init__(self, url):
        super(CovidSpider, self).__init__()
        self.start_urls = url

    def parse(self, response):

        result = CsvItem()

        result['file_urls'] = [response.url]
        yield result

def GetMobilityDatas():

    settings = Settings()

    settings.set('ITEM_PIPELINES', {'scrapy.pipelines.files.FilesPipeline': 1})
    settings.set('FILES_STORE', './data1/')
    #settings.set('FILES_RESULT_FIELD', 'covid19-mobility-data.csv')

    process = CrawlerProcess(settings)

    spider = CovidSpider

    process.crawl(spider, url = ['https://covid19-static.cdn-apple.com/covid19-mobility-data/2204HotfixDev34/v3/en-us/applemobilitytrends-2022-01-04.csv'])
    process.start()

def getMobilityDataframe():
    GetMobilityDatas()
    return pd.read_csv(glob.glob('./data/full/*.csv')[0])

if __name__ == "__main__":
    df = getMobilityDataframe()
    print(df)