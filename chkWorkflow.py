import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import getConfig as Conf
import funcoes as Func

#, "C:\\Users\\pierrefc\\Downloads\\01_wf_CRG_BI_OFERTA_CAPTACAO.XML", "C:\\Users\\pierrefc\\Downloads\\02_wf_CRG_TGT_BI_MEIO_PAGTO_REMAT_1.XML"

retPublico = []

def valida(arquivo):
    retJson = {}

    retJson.update({"Conexao":validaNomeConexao(arquivo.findAll('connectionreference'))}) 
    retJson.update({"Atributos":validaAtributos(arquivo.findAll('attribute'))})
    retJson.update({"Instancia":validaTaskInstance(arquivo.findAll('taskinstance'))})
    retJson.update({"Nome mapa":validaNomeMapa(arquivo.findAll('mapping'))})
    retJson.update({"Nome workflow":validaNomeWorkflow(arquivo.findAll('workflow'))})
    retJson.update({"Transformacoes":validaTransformations(arquivo.findAll('transformation'))})
    retJson.update({"Emails":validaTaskEmail(arquivo.findAll('task'))})
    retJson.update({"Objetos Workflow":validaObjWorkflows(arquivo.findAll('workflow'))})
    return retJson
   

def validaNomeConexao(arquivo):
    ret=[]
    retCheck = None
    conns = Conf.ListaTag("connections")
    for m in arquivo:
        if any(m['variable'] in s for s in conns):
            msg = "ok"
        else:
            msg = "nok"
        retCheck = Func.geraMensagem("Conexao {oknok} - VARIABLE {value}".format(value = m['variable'], oknok = msg), msg)
        if(retCheck != None):
            ret.append(retCheck)
    return ret
        
def validaAtributos(arquivo):
    ret=[]
    retCheck = None
    for m in arquivo:
        #7.4.1. Aumento do intervalo de commit 
        if(m['name']=="Commit Interval"):
            if(m['value']!= "10000"):
                retCheck = Func.geraMensagem("Commit Interval diferente do padrão, verificar: {v}".format(v=m['value']), "nok")
                if(retCheck != None):
                    ret.append(retCheck)
        
        #4.1.5.1. Localização dos arquivos de parâmetros
        if(m['name']=="Parameter Filename"):
            #print(m['value'])
            if(m['value'].startswith("$PMRootDir\\BWParam\\")):
                if any(m['value'].split("\\")[2] in s for s in Conf.ListaTag("nome_arquivo_param")):
                        msg = "ok"
                else:
                    msg = "nok - nome do arquivo"
            else:
                msg = "nok - nome do diretorio"
            retCheck = Func.geraMensagem("Parameter Filename {vl} {msg}".format(vl = m['value'], msg = msg), msg)
            if(retCheck != None):
                ret.append(retCheck)
    return ret

#7.4.4. Processos e re-execuções 
def validaTaskInstance(arquivo):
    ret=[]
    retCheck = None
    for m in arquivo:
        if (m.get('fail_parent_if_instance_did_not_run') is not None):
            if(m['fail_parent_if_instance_did_not_run'] !="YES"):
                retCheck = Func.geraMensagem("Task {tname} fail_parent_if_instance_did_not_run é: {v}".format(v=m['fail_parent_if_instance_did_not_run'], tname = m['taskname']), "nok")
                if(retCheck != None):
                    ret.append(retCheck)
            else:
                retCheck = Func.geraMensagem("Task {tname} fail_parent_if_instance_did_not_run ok".format(tname = m['taskname']), "ok")
                if(retCheck != None):
                    ret.append(retCheck)
        else:
            retCheck = Func.geraMensagem("Task {tname} não possui fail_parent_if_instance_did_not_run".format(tname = m['taskname']), "nok")
            if(retCheck != None):
                ret.append(retCheck)
    return ret

#Item 4.1.4.2 Nomenclatura de Mapas
def validaNomeMapa(arquivo):
    ret=[]
    retCheck = None
    for m in arquivo:
        nm = m['name'].split("_")
        msg = ""
        if(m['name'].startswith('m_') or m['name'].startswith('QW_')):
            if any(nm[1] in s for s in Conf.ListaTag("operacoes_mapa")):
                if(nm[1] == "EXT"):
                    if any(nm[2] in s for s in Conf.ListaTag("sistemas_origem")):
                        msg = "ok"
                    else:
                        msg = "nok"
            else:
                msg = "nok"
        else:
            msg = "nok"
        retCheck=Func.geraMensagem("Nome do mapa {map} está {oknok}".format(map = m['name'], oknok = msg), msg)
        if(retCheck != None):
                ret.append(retCheck)
    return ret

#4.1.4.4. Nomenclatura de Workflows 
def validaNomeWorkflow(arquivo):
    ret=[]
    retCheck = None
    for m in arquivo:
        nm = m['name'].split("_")
        msg = ""
        if(m['name'].startswith('wf_') or m['name'].startswith('QW_')):
            if any(nm[1] in s for s in Conf.ListaTag("operacoes_workflow")):
                if(len(m['name'])<31):
                    msg = "ok"
                else:
                    msg = "nok"
            else:
                msg = "nok"
        else:
            msg = "nok"
        retCheck=Func.geraMensagem("Nome do workflow {map} está {oknok}".format(map = m['name'], oknok = msg), msg)
        if(retCheck != None):
            ret.append(retCheck)
    return ret

#4.1.4.6 Transformations
def validaTransformations(arquivo):
    ret=[]
    retCheck = None
    transf = Conf.ListaTag("transformations")
    for t in transf:
        msg = ""
        for m in arquivo:
            if(m['type'] == t['tipo']):
                if(m['name'].startswith(t['nome'])):
                    msg = "ok"
                else:
                    msg = "nok"
                retCheck = Func.geraMensagem("Nome do Transformation {type} {map} está {oknok}".format(map = m['name'], oknok = msg, type = t['tipo']), msg)
                if(retCheck != None):
                    ret.append(retCheck)
    return ret

#4.1.4.7. Objetos dos Workflows
def validaObjWorkflows(arquivo):
    ret=[]
    retCheck = None
    objwf = Conf.ListaTag("objetos_workflow")
    for obj in objwf:
        msg=""
        for m in arquivo:
            tsk = m.findAll("task")
            for tk in tsk:
                if(tk['type'] == obj['tipo']):
                    if(tk['name'].startswith(obj['nome'])):
                        msg = "ok"
                    else:
                        msg = "nok"
                    retCheck= Func.geraMensagem("Workflow {wf} -> task {tsk} tipo -> {type}  está {oknok}".format(wf = m['name'], oknok = msg, type = tk['type'], tsk = tk['name']), msg)
                    if(retCheck != None):
                        ret.append(retCheck)
    return ret

#4.1.6. Uso de E-mails
def validaTaskEmail(arquivo):
    ret=[]
    retCheck = None
    for m in arquivo:
        x = m.findAll("attribute")
        if(m['type'] == "Email"):
            if(m['reusable'] == "YES"):
                if(m['name'].startswith("eml_")):
                    for eAttr in x:
                        if(not eAttr["value"].startswith("$$")):
                            retCheck=Func.geraMensagem("No email {eml} - conferir o atributo {vrl} nok".format(eml = m['name'], vrl = eAttr["name"]), "nok")
                            if(retCheck != None):
                                ret.append(retCheck)
                else:
                    retCheck=Func.geraMensagem("No email {eml} - não inicia com 'eml_' nok".format(eml = m['name']), "nok")
                    if(retCheck != None):
                        ret.append(retCheck)
            else:
                retCheck=Func.geraMensagem("No email {eml} - reusable != de YES nok".format(eml = m['name']), "nok")
                if(retCheck != None):
                    ret.append(retCheck)
    return ret