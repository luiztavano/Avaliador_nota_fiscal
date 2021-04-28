import sqlite3
import pandas as pd

class atualizar_bd_produtos(object):
    
    def __init__(self,caminho):
        
        self.caminho = caminho
        self.conn = sqlite3.connect("C:/Users/DBI5/Documents/Python/Scanner de notas/banco_de_dados.db")
        self.cursor = self.conn.cursor()
    
    def inserir_produtos(self):
        print(self.caminho)
        self.arquivo = pd.read_excel(self.caminho)
        
        self.qtde_linhas = len(self.arquivo)

        for i in range (self.qtde_linhas):
            
            self.codigo = self.arquivo.iloc[i][0]
            self.descrição = self.arquivo.iloc[i][1]
            self.preco_cheio = self.arquivo.iloc[i][2]
            self.preco_troca = self.arquivo.iloc[i][3]
            self.icms = self.arquivo.iloc[i][4]
            self.ipi = self.arquivo.iloc[i][5]
            
            self.sql = "INSERT INTO base_produtos VALUES (?,?,?,?,?,?)"
            self.cursor.execute(self.sql, 
                           [(self.codigo),(self.descrição),(self.preco_cheio),
                            (self.preco_troca),(self.icms),(self.ipi)])
        
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()  
        
        pass
    
    def apagar_produtos(self):
        
        self.sql = "DELETE FROM base_produtos"
        self.cursor.execute(self.sql)
        
        #salvar e fechar os bancos de dados
        self.conn.commit()
        self.conn.close()  
        
        pass
    
    def exportar_para_excel(self):
    
        self.sql = "SELECT * FROM base_produtos"     
        self.cursor.execute(self.sql)
        self.valor = self.cursor.fetchall()
        
        self.df = pd.DataFrame(self.valor,columns = ["Código","Descrição","Preço Cheio",
                                   "Preço Troca","Icms","Ipi"])
        
        self.nome = "/Exportar_base_produtos.xlsx"
        
        self.novo_caminho = self.caminho + self.nome
        
        self.df.to_excel (self.novo_caminho, index = False, header=True)
        
        pass
        
        