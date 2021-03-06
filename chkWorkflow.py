import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import getConfig as Conf
import funcoes as Func

#, "C:\\Users\\pierrefc\\Downloads\\01_wf_CRG_BI_OFERTA_CAPTACAO.XML", "C:\\Users\\pierrefc\\Downloads\\02_wf_CRG_TGT_BI_MEIO_PAGTO_REMAT_1.XML"

retPublico = []

def valida(arquivo, full):
    retJson = {}

    retJson.update({"Conexao":valida_nome_conexao(arquivo.findAll('connectionreference'), full)}) 
    retJson.update({"Atributos":valida_atributos(arquivo.findAll('attribute'), full)})
    retJson.update({"Instancia":valida_task_instance(arquivo.findAll('taskinstance'), full)})
    retJson.update({"Nome mapa":valida_nome_mapa(arquivo.findAll('mapping'), full)})
    retJson.update({"Nome workflow":valida_nome_wotkflow(arquivo.findAll('workflow'), full)})
    retJson.update({"Transformacoes":valida_transformations(arquivo.findAll('transformation'), full)})
    retJson.update({"Emails":valida_task_email(arquivo.findAll('task'), full)})
    retJson.update({"Objetos Workflow":valida_objeto_workflow(arquivo.findAll('workflow'), full)})
    retJson.update({"Instancia de banco":valida_instancia_banco(arquivo.findAll('instance'), full)})
    retJson.update({"Itens validados":lista_itens_manual()})
    
    return retJson
   

def valida_nome_conexao(arquivo, full):
    ret=[]
    retCheck = None
    conns = Conf.ListaTag("connections")
    for m in arquivo:
        print("valida_nome_conexao {v}".format(v=m['variable']))
        if any(m['variable'] in s for s in conns):
            msg = "ok"
        else:
            msg = "nok"
        retCheck = Func.geraMensagem("Conexao {oknok} - VARIABLE {value}".format(value = m['variable'], oknok = msg), msg, full)
        if(retCheck != None):
            ret.append(retCheck)
    return ret

#7.4.1. Aumento do intervalo de commit         
def valida_atributos(arquivo, full):
    ret=[]
    retCheck = None
    for m in arquivo:
        #7.4.1. Aumento do intervalo de commit 
        if(m['name']=="Commit Interval"):
            if(m['value']!= "10000"):
                retCheck = Func.geraMensagem("Commit Interval diferente do padrão (10000), verificar: {v}".format(v=m['value']), "nok", full)
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
            retCheck = Func.geraMensagem("Parameter Filename {vl} {msg}".format(vl = m['value'], msg = msg), msg, full)
            if(retCheck != None):
                ret.append(retCheck)
    return ret

#7.4.4. Processos e re-execuções 
def valida_task_instance(arquivo, full):
    ret=[]
    retCheck = None
    for m in arquivo:
        if (m['taskname'] != "Start"):
            if (m.get('fail_parent_if_instance_did_not_run') is not None):
                if(m['fail_parent_if_instance_did_not_run'] !="YES"):
                    retCheck = Func.geraMensagem("Task {tname} fail_parent_if_instance_did_not_run é: {v}".format(v=m['fail_parent_if_instance_did_not_run'], tname = m['taskname']), "nok", full)
                    if(retCheck != None):
                        ret.append(retCheck)
                else:
                    retCheck = Func.geraMensagem("Task {tname} fail_parent_if_instance_did_not_run ok".format(tname = m['taskname']), "ok", full)
                    if(retCheck != None):
                        ret.append(retCheck)
            else:
                retCheck = Func.geraMensagem("Task {tname} não possui fail_parent_if_instance_did_not_run".format(tname = m['taskname']), "nok", full)
                if(retCheck != None):
                    ret.append(retCheck)
    return ret

#4.1.4.2 Nomenclatura de Mapas
def valida_nome_mapa(arquivo, full):
    ret=[]
    retCheck = None
    for m in arquivo:
        nm = m['name'].split("_")
        msg = ""
        aux = ""
        if(m['name'].startswith('m_') or m['name'].startswith('QW_')):
            if any(nm[1] in s for s in Conf.ListaTag("operacoes_mapa")):
                if("srtc" not in m['name']):
                    msg = "ok"
                    if(nm[1] == "EXT"):
                        if any(nm[2] in s for s in Conf.ListaTag("sistemas_origem")):
                                msg = "ok"
                        else:
                            msg = "nok"
                            aux = " | EXT sem o nome do sistema de origem valido"
                else:
                    msg = "nok"
                    aux = " | não pode ter srtc no nome"
            else:
                msg = "nok"
                aux = " | não corresponde a lista de operacoes validas"
        else:
            msg = "nok"
            aux = " | mapa nao inicia com m_"
        retCheck=Func.geraMensagem("Nome do mapa {map} está {oknok} {aux}".format(map = m['name'], oknok = msg, aux = aux), msg, full)
        if(retCheck != None):
                ret.append(retCheck)
    return ret

#4.1.4.4. Nomenclatura de Workflows 
def valida_nome_wotkflow(arquivo, full):
    ret=[]
    retCheck = None
    for m in arquivo:
        nm = m['name'].split("_")
        msg = ""
        aux = ""
        if(m['name'].startswith('wf_') or m['name'].startswith('QW_')):
            if any(nm[1] in s for s in Conf.ListaTag("operacoes_workflow")):
                if(len(m['name'])<31):
                    msg = "ok"
                else:
                    msg = "nok"
                    aux = " | tamanho maior que 30 caracteres"
            else:
                msg = "nok"
                aux = " | não corresponde a lista de operacoes validas"
        else:
            msg = "nok"
            aux = " | workflow não inicia com wf_ ou QW_"
        retCheck=Func.geraMensagem("Nome do workflow {map} está {oknok} {aux}".format(map = m['name'], oknok = msg, aux = aux), msg, full)
        if(retCheck != None):
            ret.append(retCheck)
    return ret

#4.1.4.6 Transformations
def valida_transformations(arquivo, full):
    ret=[]
    retCheck = None
    transf = Conf.ListaTag("transformations")
    aux = ""
    for t in transf:
        msg = ""
        for m in arquivo:
            aux = ""
            if(m['type'] == t['tipo']):
                if(m['name'].startswith(t['nome'])):
                    msg = "ok"
                else:
                    msg = "nok"
                    aux = "| {map} nao inicia com {nome}".format(map = m['name'], nome = t['nome'])
                retCheck = Func.geraMensagem("Nome do Transformation {type} {map} está {oknok} {aux}".format(map = m['name'], oknok = msg, type = t['tipo'], nome = t['nome'], aux=aux), msg, full)
                if(retCheck != None):
                    ret.append(retCheck)
    return ret

#4.1.4.7. Objetos dos Workflows
def valida_objeto_workflow(arquivo, full):
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
                    retCheck= Func.geraMensagem("Workflow {wf} -> task {tsk} tipo -> {type}  está {oknok}".format(wf = m['name'], oknok = msg, type = tk['type'], tsk = tk['name']), msg, full)
                    if(retCheck != None):
                        ret.append(retCheck)
    return ret

#4.1.6. Uso de E-mails
def valida_task_email(arquivo, full):
    ret=[]
    retCheck = None
    for m in arquivo:
        x = m.findAll("attribute")
        if(m['type'] == "Email"):
            if(m['reusable'] == "YES"):
                if(m['name'].startswith("eml_")):
                    for eAttr in x:
                        if(not eAttr["value"].startswith("$$")):
                            retCheck=Func.geraMensagem("No email {eml} - conferir o atributo {vrl} nok, nao inicia com $$".format(eml = m['name'], vrl = eAttr["name"]), "nok", full)
                            if(retCheck != None):
                                ret.append(retCheck)
                else:
                    retCheck=Func.geraMensagem("No email {eml} - não inicia com 'eml_' nok".format(eml = m['name']), "nok", full)
                    if(retCheck != None):
                        ret.append(retCheck)
            else:
                retCheck=Func.geraMensagem("No email {eml} - reusable != de YES nok".format(eml = m['name']), "nok", full)
                if(retCheck != None):
                    ret.append(retCheck)
    return ret

def lista_itens_manual():
    return Func.Conf.ListaTag("topicos_validados")

def valida_instancia_banco(arquivo, full):
    ret=[]
    conns = Conf.ListaTag("instancias_banco")
    for m in arquivo:
        print(m)
        if(m.get('dbdname') == True):
            #print("dbdname in ok")
            if any(m['dbdname'] in s for s in conns):
                msg = "ok"
            else:
                msg = "nok"
            retCheck = Func.geraMensagem("Instancia de banco {oknok} - DBNAME {value}".format(value = m['dbdname'], oknok = msg), msg, full)
            if(retCheck != None):
                ret.append(retCheck)
    return ret