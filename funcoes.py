import getConfig as Conf

def geraMensagem(msg, oknok):
    msg = msg.replace("á", "a")
    
    if(oknok == "nok"):
        print(msg)
    else:
        if(oknok == "ok" and Conf.ListaTag("exibe_msg_ok") != "0"):
            print(msg)
        else:
            msg = None
    return msg