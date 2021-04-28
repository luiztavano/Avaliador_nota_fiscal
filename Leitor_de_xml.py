import xmltodict

class Leitor_xml(object):

    caminho = ""
  
    def __init__(self, caminho):
        
        self.caminho = caminho
        #self.interações = interações
        with open(self.caminho,'rb') as self.arquivo:
            self.doc = xmltodict.parse(self.arquivo)
            
    #------Valores únicos no XML-----
    def cliente(self):
        try:
            self.cliente = self.doc["nfeProc"]["NFe"]["infNFe"]["dest"]["xNome"]
        except KeyError as nfeProc:
            self.cliente = self.doc["NFe"]["infNFe"]["dest"]["xNome"]
        return self.cliente
        
    def chave(self):
        try:
            self.chave = self.doc["nfeProc"]["protNFe"]["infProt"]["chNFe"]
        except KeyError as nfeProc:
            self.chave = self.doc["NFe"]["Signature"]["SignedInfo"]["Reference"]["@URI"]
            self.chave = self.chave[4:48]
        return self.chave
    
    def cidade_cliente(self):
        try:
            self.cidade_cliente = self.doc["nfeProc"]["NFe"]["infNFe"]["dest"]["enderDest"]["xMun"]
        except KeyError as nfeProc:
            self.cidade_cliente = self.doc["NFe"]["infNFe"]["dest"]["enderDest"]["xMun"]
        return self.cidade_cliente
    
    def nota(self):
        try:
            self.nota = self.doc["nfeProc"]["NFe"]["infNFe"]["ide"]["nNF"]
        except KeyError as nfeProc:
            self.nota = self.doc["NFe"]["infNFe"]["ide"]["nNF"]
        return self.nota

    def data(self):
        try:
            self.data = self.doc["nfeProc"]["NFe"]["infNFe"]["ide"]["dhEmi"]
        except KeyError as nfeProc:
            self.data = self.doc["NFe"]["infNFe"]["ide"]["dhEmi"]
        return self.data

    def natop(self):
        try:
            self.natop = self.doc["nfeProc"]["NFe"]["infNFe"]["ide"]["natOp"]
        except KeyError as nfeProc:
            self.natop = self.doc["NFe"]["infNFe"]["ide"]["natOp"]
        return self.natop
    
    def remetente(self):
        try:
            self.remetente = self.doc["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"]
        except KeyError as nfeProc:
            self.remetente = self.doc["NFe"]["infNFe"]["emit"]["xNome"]
        return self.remetente
    
    def peso(self):
        try:
            self.peso = self.doc["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"]["pesoL"]
        except KeyError as nfeProc:
            self.peso = self.doc["NFe"]["infNFe"]["transp"]["vol"]["pesoL"]
        return self.peso
    
    def volume(self):
        try:
            self.volume = self.doc["nfeProc"]["NFe"]["infNFe"]["transp"]["vol"]["qVol"]
        except KeyError as nfeProc:
            self.volume = self.doc["NFe"]["infNFe"]["transp"]["vol"]["qVol"]
        return self.volume
    
    #------Pegar informações sobre os itens do xml-----
    def qtde_prod(self):
        try:
            self.xml = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]
        except KeyError as nfeProc:
            self.xml = self.doc["NFe"]["infNFe"]["det"]
            
        if type(self.xml) is list:
            self.qtde_prod = len(self.xml)
        else:
            self.qtde_prod = 1
        
        return self.qtde_prod

    def varios_modelo(self,interações):
        self.interações = interações
        try:
            self.modelo = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["xProd"]
        except KeyError as nfeProc:
            self.modelo = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["xProd"]   
        return self.modelo
    
    def unico_modelo(self):
        try:
            self.modelo = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["xProd"]
        except KeyError as nfeProc:
            self.modelo = self.doc["NFe"]["infNFe"]["det"]["prod"]["xProd"]
        return self.modelo
    
    def varios_codigo(self,interações):
        self.interações = interações
        try:
            self.codigo = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["cProd"]
        except KeyError as nfeProc:
            self.codigo = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["cProd"]
        return self.codigo
    
    def unico_codigo(self):
        try:
            self.codigo = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["cProd"]
        except KeyError as nfeProc:
            self.codigo = self.doc["NFe"]["infNFe"]["det"]["prod"]["cProd"]
        return self.codigo
    
    def varios_ncm(self,interações):
        self.interações = interações
        try:
            self.ncm = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["NCM"]
        except KeyError as nfeProc:
            self.ncm = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["NCM"]
        return self.ncm
    
    def unico_ncm(self):
        try:
            self.ncm = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["NCM"]
        except KeyError as nfeProc:
            self.ncm = self.doc["NFe"]["infNFe"]["det"]["prod"]["NCM"]
        return self.ncm
    
    def varios_cfop(self,interações):
        self.interações = interações
        try:
            self.cfop = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["CFOP"]
        except KeyError as nfeProc:
            self.cfop = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["CFOP"]
        return self.cfop
    
    def unico_cfop(self):
        try:
            self.cfop = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["CFOP"]
        except KeyError as nfeProc:
            self.cfop = self.doc["NFe"]["infNFe"]["det"]["prod"]["CFOP"]
        return self.cfop
    
    def varios_qtde(self,interações):
        self.interações = interações
        try:
            self.qtde = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["qCom"]
        except KeyError as nfeProc:
            self.qtde = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["qCom"]  
        return self.qtde
    
    def unico_qtde(self):
        try:
            self.qtde = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["qCom"]
        except KeyError as nfeProc:
            self.qtde = self.doc["NFe"]["infNFe"]["det"]["prod"]["qCom"]
        return self.qtde
    
    def varios_valor_unit(self,interações):
        self.interações = interações
        try:
            self.valor_unit = self.doc["nfeProc"]["NFe"]["infNFe"]["det"][self.interações]["prod"]["vUnCom"]
        except KeyError as nfeProc:
            self.valor_unit = self.doc["NFe"]["infNFe"]["det"][self.interações]["prod"]["vUnCom"]
        return self.valor_unit
    
    def unico_valor_unit(self):
        try:
            self.valor_unit = self.doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["vUnCom"]
        except KeyError as nfeProc:
            self.valor_unit = self.doc["NFe"]["infNFe"]["det"]["prod"]["vUnCom"]
        return self.valor_unit
    
    #------Pegar informações sobre a fatura do xml-----
    def qtde_parcelas(self):
        try:
            self.xml = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]
            if type(self.xml) is list:
                self.qtde_parcelas = len(self.xml)
            else:
                self.qtde_parcelas = 1
        except KeyError as cobr:
            self.qtde_parcelas = 0
        return self.qtde_parcelas
    
    def varios_valor_parcela(self,interações):
        self.interações = interações
        try:
            self.valor_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["vDup"]
        except KeyError as nfeProc:
            self.valor_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["vDup"]
        return self.valor_parcela
    
    def unico_valor_parcela(self):
        try:
            self.valor_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]["vDup"]
        except KeyError as nfeProc:
            self.valor_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"]["vDup"]
        return self.valor_parcela
    
    def varios_numero_parcela(self,interações):
        self.interações = interações
        try:
            self.numero_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["nDup"]
        except KeyError as nfeProc:
            self.numero_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["nDup"]
        return self.numero_parcela
    
    def unico_numero_parcela(self):
        try:
            self.numero_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]["nDup"]
        except KeyError as nfeProc:
            self.numero_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"]["nDup"]
        return self.numero_parcela
    
    def varios_data_parcela(self,interações):
        self.interações = interações
        try:
            self.data_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["dVenc"]
        except KeyError as nfeProc:
            self.data_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"][self.interações]["dVenc"]
        return self.data_parcela
    
    def unico_data_parcela(self):
        try:
            self.data_parcela = self.doc["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]["dVenc"]
        except KeyError as nfeProc:
            self.data_parcela = self.doc["NFe"]["infNFe"]["cobr"]["dup"]["dVenc"]
        return self.data_parcela