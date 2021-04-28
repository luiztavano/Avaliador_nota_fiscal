from pathlib import Path
from Conferencia import Conferencia
import sqlite3

class verificar_xml(object):
    
        def __init__(self):
        
            #definição dos caminhos e variáveis
            self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
            self.cursor = self.conn.cursor()
            
            self.sql = "SELECT * FROM caminho_diretorio"
            self.cursor.execute(self.sql)
            self.caminho = self.cursor.fetchall()
            self.caminho_diretorio = self.caminho[0][0]
            
        def verificacao(self):
            
            self.notas = []
            
            #loop para conferir todas os xml da pasta
            for self.path in Path(self.caminho_diretorio).rglob('*.xml'):
    
                self.chave = self.path.name
                self.valor = self.chave[45:48]
    
                #verificar se o xml é de uma nota fiscal
                if self.valor == "nfe":
                    
                    #separar o trecho com a numeração do xml
                    self.chave = self.chave[0:44]
                   
                    #consultar se a chave já está inserida na base principal
                    self.sql = "SELECT * FROM xml WHERE chave=?"
                    self.cursor.execute(self.sql, [(self.chave)])
                    self.retorno1 = self.cursor.fetchall()

                    #consultar se a chave já está inserida na base provisória
                    self.sql = "SELECT * FROM xml_provisoria WHERE chave=?"
                    self.cursor.execute(self.sql, [(self.chave)])
                    self.retorno2 = self.cursor.fetchall()
                    
                    #verificar se a chave não está inserida nas duas bases                
                    if self.retorno1 == [] and self.retorno2 == []:
                        
                        #realizar a verificação do xml
                        self.xml = Conferencia(self.path)  
                        self.fatura = self.xml.verificar_fatura()
                        
                        for x in self.fatura:
                            self.notas.append(x)
                            
                        # self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
                        # self.cursor = self.conn.cursor()
                        
                        # print(self.chave)
                        #inserir o xml na base provisória
                        self.sql = "INSERT INTO xml_provisoria VALUES (?)"
                        self.cursor.execute(self.sql, [(self.chave)])

            #salvar e desconectar do banco de dados
            self.conn.commit()
            self.conn.close()        
            
            #retorno da lista de xml com problemas
            return self.notas


