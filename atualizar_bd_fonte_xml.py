import sqlite3

class atualizar_bd_fonte_xml(object):
    
    def __init__(self,caminho):
        
        self.caminho = caminho
        self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
        self.cursor = self.conn.cursor()
    
    def atualizar(self):
        
        self.sql = "DELETE FROM caminho_diretorio"
        self.cursor.execute(self.sql)
            
        self.sql = "INSERT INTO caminho_diretorio VALUES (?)"
        self.cursor.execute(self.sql,[(self.caminho)])
        
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()  
   
    
        