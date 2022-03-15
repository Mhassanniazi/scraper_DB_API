# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class HassanscraperPipeline:
    # constructore/initializer which gets executes everytime class instantiate
    def __init__(self):
        self.create_connection()
        self.create_tables()
    # making sqlite (database) connection
    def create_connection(self):
        self.conn = sqlite3.connect("scraper.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        print("ABOUT CONNECTION:",self.cursor)
    def create_tables(self): 
        print("Create table function chala")
        # here condition is "if not exists" bcz everytime this class called so condition
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS QUOTES (ID INTEGER PRIMARY KEY, QUOTE TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS RESULTS (ID INTEGER PRIMARY KEY, RES_ID INTEGER, AUTHOR TEXT, TAGS TEXT, FOREIGN KEY (RES_ID) REFERENCES QUOTES (ID))""")
    def process_item(self, item, spider):
        print("Process_item function chala")
        self.save_to_db(item)
        return item
    def save_to_db(self,item):
        print("I GOT EXECUTED TOO")
        self.cursor.execute("""INSERT INTO QUOTES VALUES(?,?)""",(int(item['pkk']),item['quote']))
        # here explicitely send null, as PK could not be null so replaced by unique numbers
        self.cursor.execute("""INSERT INTO RESULTS VALUES(null,?,?,?)""",(int(item['pkk']),item['author'],','.join(item['tags'])))
        self.conn.commit()

        # print("pipeeALL",item)
        # print("pipee",item['quote'])