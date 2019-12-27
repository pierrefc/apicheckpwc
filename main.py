import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import chkWorkflow as WF
import getConfig as Conf

#4034 rtm

def ExecutaCheck(arquivo):
    soup = BeautifulSoup(arquivo, "lxml")
    return WF.valida(soup)        

def main():
    arquivo = Conf.ListaTag("arquivos")
    for m in arquivo:
        print("## Inicia validação do arquivo {file}".format(file = m))
        parseLog(m)

def parseLog(file):
        data = ""
        with open(file, "r") as f:
                data = f.read()
                f.close()
        soup = BeautifulSoup(data, "lxml")
        WF.valida(soup)

if __name__ == "__main__":
    main()