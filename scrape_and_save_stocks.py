import pymongo
import sys
import requests
import datetime
import time
import os


class MongoDB:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient('mongodb://admin:password@mongodb:27017')
            print ('Connected to MongoDB succesfully')
        except:
            print ('ERROR: make sure that database is up and running')
            sys.exit()
    
    def __create_database__(self):
         self.database = self.client['yahoo-data']
         self.database.create_collection('stock-prices')
    
    def __check_existance__(self, name):
        return True if name in self.client.list_database_names() else False
    
    def put(self, name, market_time, price, timestamp):
        if self.__check_existance__('yahoo-data') == False:
            self.__create_database__()
        
        self.database = self.client['yahoo-data']
        self.collection = self.database['stock-prices']
    
        self.data = {   
                        'company_name' : name,
                        'market_time': market_time,
                        'stock_price' : price,
                        'timetamp' : timestamp
                    }
        
        self.collection.insert_one(self.data)
       
class FetchData:
    
    def __init__(self, brand):
 
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.web = f'https://query1.finance.yahoo.com/v8/finance/chart/{brand}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance' 

    def generate_data_dictionary(self):
            self.trigger = True
            self.response = requests.get(self.web, headers = self.headers)
            while self.trigger:
                if self.response.status_code == 200:
                    return self.response.json()['chart']['result'][0]['meta']
    
    def run(self):
        self.data = self.generate_data_dictionary()
        self.mongo = MongoDB()
        self.mongo.put( self.data['symbol'],
                        self.data['regularMarketTime'],
                        self.data['regularMarketPrice'],
                        str(datetime.datetime.now())
        )

while True:
    yahoo = FetchData('TSLA')
    yahoo.run()