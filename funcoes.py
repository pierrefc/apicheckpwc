import getConfig as Conf



def geraMensagem(msg, oknok, full):
    msg = msg.replace("á", "a")
    
    if(oknok == "nok"):
        print(msg)
    else:
        if(oknok == "ok" and full != "0"):
            print(msg)
        else:
            msg = None
    return msg