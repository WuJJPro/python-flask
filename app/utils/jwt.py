import base64
import json

def get_userid(jwt:str):
    origStr = jwt.split(".")[1]
    if (len(origStr) % 3 == 1):
        origStr += "=="
    elif (len(origStr) % 3 == 2):
        origStr += "="
    res = str(base64.b64decode(origStr),"utf-8")
    res_json = json.loads(res)
    return res_json["aud"][0]