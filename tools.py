from database import get_connection
import operator
import re

#Tools to perform

#to save in database
def tool_savememory(key:str,value:str):

    try:
        with get_connection() as connect:
            with connect.cursor() as cur:
                cur.execute("select * from memorydata where key=%s",(key,))
                res=cur.fetchone()

                if res:
                    cur.execute("update memorydata SET value=%s where key=%s",(value,key))

                else:
                    cur.execute("Insert into memorydata (key,value) values (%s,%s)",(key,value))

        return {"key":key,"value":value}

    except Exception as e:
         return {"error": f"Database error: {e}"}
        


#to get from database
def tool_getmemory(key:str):
    with get_connection() as connect:
        with connect.cursor() as cur:
            try:
                cur.execute("select value from memorydata where key=%s",(key,))
                result=cur.fetchone()

                if result:
                    return{"key":key,"value":result[0]}
                else:
                    return{"key":key,"value":None}

            except Exception as e:
                return {"error": f"Database error: {e}"}


#to calculate

ops = {
    "plus": operator.add,
    "minus": operator.sub,
    "times": operator.mul,
    "divided by": operator.truediv
}
def tool_Calculate(text:str):
    s=text.lower()
    s=s.replace("what is", "").replace("calculate", "").strip()

    numbers = re.findall(r"\d+", s)



    if len(numbers) < 2:
        return {"error": "Not enough numbers"}

    a, b = map(int, numbers)


    word= None
    for key in ops.keys():
        if key in text:
            word = key
            break


    if not word:
        return {"error": "Unknown operator"}

    

    try:
        result=ops[word](a,b)
        return{"expression": f"{a} {word} {b}", "result": result}

    except:
        return{"error":"Could not calculate"}