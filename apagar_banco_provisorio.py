import sqlite3

class apagar_banco_provisorio(object):
    
    def __init__(self):
            
        #definição dos caminhos e variáveis
        self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
        self.cursor = self.conn.cursor()

    def apagar(self):
        #deletar todos os xml do banco provisório
        self.sql = "DELETE FROM xml_provisoria"
        self.cursor.execute(self.sql)
        
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()  
        
