import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import chkWorkflow as WF
import getConfig as Conf

#4034 rtm

def ExecutaCheck(arquivo):
    soup = BeautifulSoup(arquivo.data, "lxml")
    full = arquivo.headers.get('full')
    if (full == None):
        full = 0
    print("-----------------------")
    print(full)
    print(arquivo.headers.get('full'))
    print("-----------------------")

    return WF.valida(soup, full)

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