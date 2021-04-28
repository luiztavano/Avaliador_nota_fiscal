from Leitor_de_xml import Leitor_xml
import sqlite3


class conferir_preco_e_tributacao(object):
    
    path=""
    
    def __init__(self,caminho):
        
        self.path = caminho
        self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
        self.cursor = self.conn.cursor()
    
    def pegar_produto_preco_errado(self):
        
        #qtde de produtoes diferentes na nota
        self.xml = Leitor_xml(self.path)
        self.n_produtos = int(self.xml.qtde_prod())
        self.resultado_final =[]
        
        for i in range(self.n_produtos):
            self.xml = Leitor_xml(self.path)
            self.nota = self.xml.nota()
            self.cliente = self.xml.cliente()
            self.cidade = self.xml.cidade_cliente()
            self.chave = self.xml.chave()
            self.data = self.xml.data()
            
            if self.n_produtos == 1:
                self.codigo = self.xml.unico_codigo()
                self.descricao = self.xml.unico_modelo()
                self.preco_produto = float(self.xml.unico_valor_unit())
            
            else:
                self.codigo = self.xml.varios_codigo(i)
                self.descricao = self.xml.varios_modelo(i)
                self.preco_produto = float(self.xml.varios_valor_unit(i))
            
            self.sql = "SELECT * FROM base_produtos WHERE Codigo=?"
            self.cursor.execute(self.sql, [(self.codigo)])
            self.resultado_consulta = self.cursor.fetchall()
            
            
            if self.resultado_consulta == []:
                self.resultado = [self.data,self.chave,self.nota,self.cliente,self.cidade,
                                  self.codigo,self.descricao,self.preco_produto,"Item não cadastrado",""]
            
            else:
               
                if self.resultado_consulta[0][2] == "":
                    self.resultado_consulta[0][2] = self.resultado_consulta[0][3]
                    
                self.valor_tabela_troca = self.resultado_consulta[0][2]
                self.valor_tabela_cheio = self.resultado_consulta[0][3]
                
                self.coeficiente_troca = abs(1-(self.preco_produto/self.valor_tabela_troca))
                self.coeficiente_cheio = abs(1-(self.preco_produto/self.valor_tabela_cheio))
                
                self.diferenca_troca = abs(self.preco_produto-self.valor_tabela_troca)
                self.diferenca_cheio = abs(self.preco_produto-self.valor_tabela_cheio)
                
                if self.diferenca_troca <= self.diferenca_cheio:
                    self.referencia = self.valor_tabela_troca
                
                else:
                    self.referencia = self.valor_tabela_cheio
                                      
                if self.coeficiente_troca > 0.05 and self.coeficiente_cheio > 0.05:  
                    self.ok = "ok"
                    self.resultado = [self.data,self.chave,self.nota,self.cliente,self.cidade,
                                      self.descricao,self.preco_produto,self.referencia,"Nota emitida com o preço incorreto",""]
                    self.resultado_final.append(self.resultado)                      
                else:
                    self.resultado = []
                    self.resultado = [self.data,self.chave,self.nota,self.cliente,self.cidade,
                                      self.descricao,self.preco_produto,self.referencia,"Nota emitida com o preço correto",""]
                    #print(self.resultado)                
                    
            #self.resultado_final.append(self.resultado)
        
        return self.resultado_final
