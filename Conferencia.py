from Leitor_de_xml import Leitor_xml
from conferir_preco_tributacao import  conferir_preco_e_tributacao

class Conferencia(object):

    caminho = ""
    def __init__(self,caminho):
        
        #definição das variáveis que serão utilizadas
        self.caminho = caminho
        self.xml = Leitor_xml(self.caminho)
        self.natop = self.xml.natop()
        self.fatura = self.xml.qtde_parcelas()
        self.nota = self.xml.nota()
        self.cliente = self.xml.cliente()
        self.cidade = self.xml.cidade_cliente()
        self.resultado_final = []
        self.chave = self.xml.chave()
        self.data = self.xml.data()
        
    def verificar_fatura(self):
        
        #verificar se o xml é de uma nota de venda
        if (self.natop == "VENDA DE MERCADORIA" or 
        self.natop == "VENDA DE MERCADORIAS" or 
        self.natop == "FATURAMENTO PARA ENTREGA FUTURA"): 
        
            #verificar se o xml não possui fatura
            if self.fatura == 0:
                
                #se não possuir, inserir na lista de retorno de xml com problemas
                self.resultado = [self.data,self.chave,self.nota,self.cliente,
                                  self.cidade,"","","","Nota fiscal de " + self.natop + " emitida sem fatura",""]
                self.resultado_final.append(self.resultado)
                
            #se o xml possuir fatura
            else: 
                
                #passar para a conferência de valores e de tributação
                self.conferencia_preco = conferir_preco_e_tributacao(self.caminho)                
                self.resultado = self.conferencia_preco.pegar_produto_preco_errado()
                
                #inserir retorno na lista de xml com problemas
                for i in self.resultado:
                   self.resultado_final.append(i)  
        
        #caso o xml não seja de uma nota de venda
        else:
            
            #verificar o xml possui fatura
            if self.fatura > 0:
                
                #se possuir, inserir na lista de retorno de xml com problemas
                self.resultado = [self.data,self.chave,self.nota,self.cliente,
                                  self.cidade,"","","", "Nota fiscal de " + self.natop + " emitida com fatura",""]
                self.resultado_final.append(self.resultado)

        #retorno da lista de xml com problemas
        return self.resultado_final
        
        
        
    
