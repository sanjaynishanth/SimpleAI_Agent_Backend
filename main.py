from fastapi import FastAPI
from models import Data
from tools import tool_savememory,tool_getmemory,tool_Calculate
import re
from database import table_ensure


table_ensure()

app=FastAPI()



#API End Point  

@app.get("/")
def check():
    return {"Its working"}
    

@app.post("/agent/read_query")

def read_input(data: Data):

    if not data.text or len(data.text.strip()) < 2:
        return {"error": "Empty or invalid prompt"}


    try:

        text=data.text.lower()


        # store in memory
        if "remember" in text:
            try:
                text=text.replace("remember","").strip()
                text=text.replace("my","").strip()

                values=text.split(" is ")
                key=values[0].strip()
                value=values[1].strip()
                resp=tool_savememory(key,value)
                # resp=f"Memory saved {value}"

                return{
                    "original prompt":data.text,
                    "Choosen tool":"memory_save",
                    "tool_input":{"key":key,"Value":value},
                    "response":resp

                }

            except:
                return{"error":"Invalid format"}

        #get from memory

        if "what is my" in text or "recall" in text:
            try:
                text=text.replace("what is my","").replace("recall","").replace("?","").strip()
                key=text
                resp=tool_getmemory(key)

                return{
                    "original prompt":data.text,
                    "Choosen tool":"memory_read",
                    "tool_input":key,
                    "response":resp
                }

            except:
                return{"error":"Invalid format to fetch from memory"}


        # handle calculation

        found_digit=False
        if re.search(r"\d",text):
            found_digit=True
        
        found_word=False
        for w in ["plus","minus","times","divided by"]:
            if w in text:
                found_word=True
                break

        if found_digit and found_word:

            res=tool_Calculate(text)

            return{
                "original prompt":data.text,
                "Choosen tool":"Calculator",
                "tool_input":text,
                "response":res

            }

        return {"error":"I dont hava the tool"}

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}

