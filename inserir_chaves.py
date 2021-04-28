import sqlite3

class inserir_chaves(object):
    
    def __init__(self, chaves):
            
             #definição dos caminhos e variáveis
            self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
            self.cursor = self.conn.cursor()
            self.chaves = chaves
            
    def inserir(self):
        
        #loop para inserir todas as chaves no banco principal
        for i in self.chaves:
            
            self.sql = "INSERT INTO xml VALUES (?)"
            self.cursor.execute(self.sql, [(i)])
            
            
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()      
          
        #conectar com o banco de dados provisório
        self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
        self.cursor = self.conn.cursor()
        
        #loop para deletar todas as chaves inseridas no principal do banco provisório
        for i in self.chaves:
            
            self.sql = "DELETE FROM xml_provisoria WHERE chave = ?"
            self.cursor.execute(self.sql, [(i)])
            print(i)
        
        # #deletar todos os xml do banco provisório
        # self.sql = "DELETE FROM xml_provisoria"
        # self.cursor.execute(self.sql)
        
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()  
            
        pass
        

