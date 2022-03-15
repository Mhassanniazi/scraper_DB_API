from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from hassanScraper.pipelines import HassanscraperPipeline

# creating data model which act as a request body
class Quotes(BaseModel):
    quote: str
    author: str
    tags: Optional[str]

app = FastAPI()

# database connection 
dbCon = HassanscraperPipeline()

@app.get("/quotes")
def Show_quotes():
    print("CHECKING CONN:",dbCon)
    quotesData = dbCon.cursor.execute("""SELECT * FROM QUOTES""").fetchall()
    for i in range(len(quotesData)):
        jsonData = {}
        jsonData['id'] = quotesData[i][0]
        jsonData['quote'] = quotesData[i][1]

        quotesData[i] = jsonData
    return quotesData

@app.get("/result")
def Show_results():
    resultData = dbCon.cursor.execute("""SELECT * FROM RESULTS""").fetchall()
    for i in range(len(resultData)):
        jsonData = {}
        jsonData['id'] = resultData[i][0]
        jsonData['author'] = resultData[i][2]
        jsonData['tags'] = resultData[i][3]

        resultData[i] = jsonData
    return resultData
    
@app.post("/add")
def add_quotes(item: Quotes):
    print("Checking return data:",item," and type ",type(item))
    a=item.dict()
    print("HELLO:",a,"and type is: ",type(a))
    # must use "," after var inside tuple for single value
    dbCon.cursor.execute("""INSERT INTO QUOTES VALUES(null,?)""",(item.quote,))
    allData = dbCon.cursor.execute("""SELECT * FROM RESULTS""").fetchall()
    dbCon.cursor.execute("""INSERT INTO RESULTS VALUES(null,?,?,?)""",(int(allData[-1][1])+1,item.author,item.tags))
    dbCon.conn.commit()

    return {"Succes":"Succesfully Inserted"}

