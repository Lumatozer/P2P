import json
def filter(msg,query):
    message=dict(json.loads(msg))
    try:
        return message[query]
    except:
        return False