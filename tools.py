from database import get_connection
import operator
import re
import ast

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
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def safe_eval(node):
    
    
    if isinstance(node, ast.Constant):  # handles numbers
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Only numeric constants are allowed")

    elif isinstance(node, ast.BinOp):  # binary operation (+, -, *, /, **)
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in ops:
            return ops[op_type](left, right)
        else:
            raise ValueError(f"Unsupported operator: {op_type}")

    elif isinstance(node, ast.UnaryOp):  # negative numbers (-5)
        op_type = type(node.op)
        if op_type in ops:
            return ops[op_type](safe_eval(node.operand))
        else:
            raise ValueError(f"Unsupported unary operator: {op_type}")

    else:
        raise ValueError(f"Invalid or unsupported expression node: {type(node)}")




def tool_Calculate(text:str):
    s=text.lower()
    s=s.replace("what is", "").replace("calculate", "").strip()

    s = (
        s.replace("plus", "+")
        .replace("minus", "-")
        .replace("times", "*")
        .replace("divided by", "/")
        .replace("x", "*")
    )
    s = re.sub(r"[^0-9\+\-\*\/\.\(\)\s]", "", s)

    

    try:
        node=ast.parse(s,mode="eval").body
        result=safe_eval(node)

        return{"expression":s, "result": result}

    except Exception as e:
        return{"error":f"Invalid expression:{str(e)}"}