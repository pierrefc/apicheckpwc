import json

def ValidaDevOps(ret):
    #print('|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@|@')
    for x, y in ret.items():
        #print('--- {a} ---'.format(a=y))
        if(len(y) > 0):
            for valor in y:
                if("nok" in valor):
                    return 0
    return 1