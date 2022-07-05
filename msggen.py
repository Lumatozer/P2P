def gen(data,uid):
    import json
    return str(json.dumps({"type":"relay","data":data.decode(),"uid":str(uid)}))