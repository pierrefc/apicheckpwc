import json

def LeConfig():
    f= open("checkpwc_config.json", "r")
    if f.mode == "r":
        return f.read()

def ListaTag(sTag):
    lt = LeConfig()
    ljson = json.loads(lt)
    return ljson[sTag]
