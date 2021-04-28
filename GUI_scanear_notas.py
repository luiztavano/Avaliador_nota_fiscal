#bibliotecas utilizadas do sistema
import sys
from datetime import date

#Pyqt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#classes criadas
from inserir_chaves import inserir_chaves
from apagar_banco_provisorio import apagar_banco_provisorio
from scanner import verificar_xml
from atualizar_bd_fonte_xml import atualizar_bd_fonte_xml
from Atualizar_base_produtos import atualizar_bd_produtos

#Definição da janela
class Window(QWidget):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        
        #Configuração da janela
        self.setWindowTitle('Scanner de notas')
        self.setGeometry(200, 300, 1100, 300)
        
        #Criação dos campos
        self.label=QLabel('Scannear XML das notas emitidas')
        self.horario=QLabel('Hora')
        self.Status=QLabel('Escaneamento não iniciado...')
        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')
        self.baixar=QPushButton('Baixar')

        #Criação dos botões da lista no menu
        self.btn_atualizarbase = QAction("Atualizar base de preços", self)
        self.btn_atualizarbase.triggered.connect(self.window_atualizar_base)
        
        self.btn_base_xml = QAction("Selecionar caminho base de XML's", self)
        self.btn_base_xml.triggered.connect(self.window_caminho_xml)
        
        #Criar a barra de menu superior
        self.menubar = QMenuBar()
        self.actionFile = self.menubar.addMenu("Outras funções")
        self.actionFile.addAction(self.btn_atualizarbase)
        self.actionFile.addAction(self.btn_base_xml)
        
        #Conexão dos botões
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.baixar.clicked.connect(self.baixar_notas)
        
        #Configuração do looping
        self.timer= QTimer()
        self.timer.timeout.connect(self.verificacao)
        self.timer.timeout.connect(self.showTime)
        
        #Criação da tabela
        self.tabela = self.createTable()
        
        #Exibir o layout
        self.exibir_layout = self.layout()

        
    def layout(self):
        
        #Adicionar os botões no groupbox
        layout1 = QHBoxLayout()
        layout1.addWidget(self.startBtn)
        layout1.addWidget(self.endBtn)
        layout1.addWidget(self.baixar)
        
        #Espaçamento dos botões
        layout1.addStretch(1)
        
        #Configurar o groupbox
        groupBox = QGroupBox()
        groupBox.setLayout(layout1)
        
        #Adicionar itens no layout da janela
        layout = QVBoxLayout()
        layout.addWidget(self.menubar)
        layout.addWidget(self.horario)
        layout.addWidget(self.label)
        layout.addWidget(self.Status)
        layout.addWidget(groupBox)
        layout.addWidget(self.tableWidget)
        
        #Ativar layout
        self.setLayout(layout)
        
    def verificacao(self):
        
        #Executar verificação de xml
        self.executar = verificar_xml()
        
        #Lista contendo xml com problemas
        self.notas = self.executar.verificacao()
        
        #Verificar se a lista de xml não está vazia
        if len(self.notas) > 0:
            
            #Se não estiver, exibir alerta
            #Configuração da janela de alerta
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Foram encontrados pedidos com possíveis erros")
            self.msgBox.setWindowTitle("Aviso")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            
            #Se a janela estiver minimizada, restaurar-la
            if self.windowState() == Qt.WindowMinimized:
                
                # Window is minimised. Restore it.
                self.setWindowState(Qt.WindowActive)
             
            #Exibir janela
            returnValue = self.msgBox.exec()
            
            #Se clicar no botão ok, não fazer nada
            if returnValue == QMessageBox.Ok:
                 pass           
        
        #Laço para inserir lista na tabela
        for i in range(len(self.notas)):
            
            #Contagem de linhas atual da tabela
            linha = self.tableWidget.rowCount()
            
            #Inserir uma linha
            self.tableWidget.insertRow(linha)
            
            #Formatar data da nota
            data = self.notas[i][0]
            dia = data[8:10]
            mes = data[5:7]
            ano = data[0:4]
            data_arrumada = dia+"/"+mes+"/"+ano
            
            #Inserir informações da lista de xml na tabela
            self.tableWidget.setItem(linha,0, QTableWidgetItem(data_arrumada))
            self.tableWidget.setItem(linha,1, QTableWidgetItem(self.notas[i][1]))
            self.tableWidget.setItem(linha,2, QTableWidgetItem(self.notas[i][2]))
            self.tableWidget.setItem(linha,3, QTableWidgetItem(self.notas[i][3]))
            self.tableWidget.setItem(linha,4, QTableWidgetItem(self.notas[i][4]))
            self.tableWidget.setItem(linha,5, QTableWidgetItem(self.notas[i][5]))
            self.tableWidget.setItem(linha,6, QTableWidgetItem(str(self.notas[i][6])))
            self.tableWidget.setItem(linha,7, QTableWidgetItem(str(self.notas[i][7])))
            self.tableWidget.setItem(linha,8, QTableWidgetItem(self.notas[i][8]))
            
            #Criar um checkbox e inserir na tabela
            ch = QCheckBox()
            self.tableWidget.setCellWidget(linha, 9, ch)
            self.valor="False"
            self.tableWidget.setItem(linha,9, QTableWidgetItem(self.valor))
            self.tableWidget.item(linha, 9).setForeground(QColor(255, 255, 255))
            
            #Conectar função ao clicar no checkbox
            ch.clicked.connect(self.onStateChanged)
            
    def baixar_notas(self):
        
        #Parar temporizador
        self.timer.stop()
        
        #Criar lista para inserir xml baixados
        self.notas_a_baixar = []
        
        #Contar qtde. de linhas atual da tabela
        self.linha = self.tableWidget.rowCount()
        
        #looping para percorrer todas as linhas da tabela
        i = 0
        while i <(self.linha):
            
            #tentar verificar conteúdo da célula
            try:
                self.check = self.tableWidget.item(i,9).text()
            
            #caso dê erro, pular para próxima linha
            except (AttributeError):
                i = i + 1
                pass
            
            #Caso não haja erro...
            else:
                
                #Verificar se o conteúdo da célula significa que o checkbox está marcado
                if self.check == "True":
                    
                    #Caso esteja, pegar a numeração da chave
                    self.chave = self.tableWidget.item(i,1).text()
                    
                    #Inserir na lista de xml que serão baixados
                    self.notas_a_baixar.append(self.chave)
                    
                    #Apagar linha
                    self.tableWidget.removeRow(i)
                    
                    #Contar novamente a qtde. de linha da tabela
                    self.linha = self.tableWidget.rowCount()
                
                #Se o checkbox não estiver marcado...
                else:
                    
                    #Pular para próxima linha
                    i = i + 1

        #Remover chaves duplicadas da lista
        self.notas_a_baixar = list(dict.fromkeys(self.notas_a_baixar))
        
        # print(self.notas_a_baixar)  
        #Chamar a função que vai inserir as chaves no banco principal
        self.notas_baixadas = inserir_chaves(self.notas_a_baixar)

        #Inserir chaves
        self.notas_baixadas.inserir()
        
            
    def onStateChanged(self): #Método para preencher célula conforme alteração do checkbox

        #Definir variável
        ch = self.sender()
                
        #Pegar posição da célula correspondente ao checkbox
        ix = self.tableWidget.indexAt(ch.pos())
        
        #Verificar se a célula referente possui algum valor
        try:
            self.valor_celula = self.tableWidget.item(ix.row(),9).text()
            
        #Se encontrar erro, assumir a célula como vazia    
        except (AttributeError):   
            self.valor_celula = self.tableWidget.item(ix.row(),9)
            
        #Se a célula estiver com "True" significa que o checkbox está marcado
        if self.valor_celula == 'True':
            
            #Alterar a variável para "False", pois o checkbox foi desmarcado
            self.valor = QTableWidgetItem('False')
            self.valor.setForeground(QColor(255, 255, 255)) 
        #Se a célula não estiver com "True", o checkbox está desmarcado
        else:
            
            #Alterar a variável para "True", pois o checkbox foi marcado
            self.valor = QTableWidgetItem('True')
            self.valor.setForeground(QColor(255, 255, 255))

        #Preencher a célula corresponde ao checkbox com o novo valor da variável
        self.tableWidget.setItem(ix.row(),9, self.valor)
        #self.tableWidget.item(ix.row(), 9).setForeground(QColor(255, 255, 255))
        
    def closeEvent(self,event):
        
        #Exibir mensagem de confirmação de fechamento
        self.quit_msg = "Are you sure you want to exit the program?"
        self.reply = QMessageBox.question(self, 'Message', 
                                           self.quit_msg, QMessageBox.Yes, QMessageBox.No)

        #Se confirmar o desejo de fechar...
        if self.reply == QMessageBox.Yes:
            
            #Parar temporizador
            self.timer.stop()
        
            #Exibir mensagem
            self.Status.setText("Fechando programa...")
        
            #Chamar função e apagar banco provisório
            self.apagar = apagar_banco_provisorio()
            self.apagar.apagar()
        
            #Fechar janela
            self.close()
        
        #Caso não confirmar, não fazer nada
        else:
            event.ignore()
        
    def startTimer(self,checked):
        #Minimizar a janela
        self.setWindowState(Qt.WindowMinimized)
        
        #Definir frequência do temporizador
        self.timer.start(1000)
        
        #Ativar e desativar botões
        self.startBtn.setEnabled(False)
        self.baixar.setEnabled(False)
        self.actionFile.setEnabled(False)
        self.endBtn.setEnabled(True)
        
        #Exibir mensagem
        self.Status.setText("Escaneamento iniciado...")

    def endTimer(self):
        #Parar temporizador
        self.timer.stop()
        
        #Ativar e desativar botões
        self.startBtn.setEnabled(True)
        self.baixar.setEnabled(True)
        self.actionFile.setEnabled(True)
        self.endBtn.setEnabled(False)
        
        #Exibir mensagem
        self.Status.setText("Escaneamento parado...")
        
    def createTable(self): 
        #Criar a tabela
        self.tableWidget = QTableWidget() 
  
        #Contagem de linhas e colunas
        self.tableWidget.setRowCount(0)  
        self.tableWidget.setColumnCount(10)
   
        #Definição dos cabeçalhos e ajuste com a tela
        self.tableWidget.setHorizontalHeaderLabels(["Data","Chave","Nota","Cliente","Cidade","Descrição",
                                                    "Valor","Valor tab.", "Status","Check"])
        
        #Definição dos tamanhos das colunas
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 250)
        self.tableWidget.setColumnWidth(4, 150)
        self.tableWidget.setColumnWidth(5, 250)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 80)
        self.tableWidget.setColumnWidth(8, 300)
        self.tableWidget.setColumnWidth(9, 50)
        
        
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def showTime(self):
        #Pegar horário do sistema
        time=QDateTime.currentDateTime()
        
        #Formatar exibição do horário
        timeDisplay=time.toString('dd/MM/yyyy hh:mm:ss dddd')
        
        #Exibir
        self.horario.setText(timeDisplay)
        
    def window_atualizar_base(self):
        self.w = Window_atualizar_base()
        self.w.show()
    
    def window_caminho_xml(self):
        self.w = Window_caminho_base_xml()
        self.w.show()
    
#Definição da janela
class Window_atualizar_base(QWidget):
    def __init__(self,parent=None):
        super(Window_atualizar_base, self).__init__(parent)
        
        #Configuração da janela
        self.setWindowTitle('Atualizar banco de dados')
        self.setGeometry(200, 300, 450, 160)
        #self.setWindowFlags(Qt.WindowMaximizeButtonHint |Qt.WindowMinimizeButtonHint )
        
        #Criação dos campos
        self.label=QLabel('Atualizar Base de Produto')
        
        self.qline_importar=QLineEdit()
        self.btn_sel_arquivo=QPushButton("Selecionar")
        self.btn_importar=QPushButton("Importar")
        
        self.qline_exportar=QLineEdit()
        self.btn_sel_diretorio=QPushButton("Selecionar")
        self.btn_exportar=QPushButton("Exportar")
        
        self.label_deletar=QLabel('Apagar base')
        self.btn_deletar=QPushButton("Deletar")
        
        #Conexão dos botões
        self.btn_sel_arquivo.clicked.connect(self.selecionar_arquivo)
        self.btn_sel_diretorio.clicked.connect(self.selecionar_diretorio)
        
        self.btn_importar.clicked.connect(self.importar)
        self.btn_exportar.clicked.connect(self.exportar)
        self.btn_deletar.clicked.connect(self.deletar)
                
        #Exibir o layout
        self.exibir_layout = self.layout()
        
    def layout(self):
        
        #Adicionar os itens no groupbox1
        layout1 = QHBoxLayout()
        layout1.addWidget(self.btn_sel_arquivo)
        layout1.addWidget(self.btn_importar)
        layout1.addStretch(1)
        
        #Configurar o groupbox
        groupBox1 = QGroupBox('Selecione o arquivo de importação')
        groupBox1.setLayout(layout1)
        
        #Adicionar os itens no groupbox2
        layout2 = QHBoxLayout()
        layout2.addWidget(self.btn_sel_diretorio)
        layout2.addWidget(self.btn_exportar)
        layout2.addStretch(1)
        
        #Configurar o groupbox
        groupBox2 = QGroupBox('Selecione o diretório de exportação')
        groupBox2.setLayout(layout2)
        
        #Adicionar os itens no groupbox2
        layout3 = QHBoxLayout()
        layout3.addWidget(self.btn_deletar)
        layout3.addStretch(1)
        
        #Configurar o groupbox
        groupBox3 = QGroupBox('Apagar toda a base de dados')
        groupBox3.setLayout(layout3)
        
        #Adicionar itens no layout da janela
        layout_final = QVBoxLayout()
        layout_final.addWidget(self.label)
        layout_final.addWidget(groupBox1)
        layout_final.addWidget(self.qline_importar)
        layout_final.addWidget(groupBox2)
        layout_final.addWidget(self.qline_exportar)
        layout_final.addWidget(groupBox3)
        
        #Ativar layout
        self.setLayout(layout_final)
        
    def selecionar_arquivo(self):

        self.file = QFileDialog.getOpenFileName(self, "Selecione o arquivo")
        self.qline_importar.setText(self.file[0])
        
    def selecionar_diretorio(self):

        self.file = QFileDialog.getExistingDirectory(self, "Selecione o diretório")
        self.qline_exportar.setText(self.file)
        
    def importar(self):
        
        self.base = atualizar_bd_produtos(self.qline_importar.text())
        self.base.inserir_produtos()
        
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Importação realizada com sucesso")
        self.msgBox.setWindowTitle("Mensagem")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec()
        
    def exportar(self):
        
        self.base = atualizar_bd_produtos(self.qline_exportar.text())
        self.base.exportar_para_excel()
                
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText("Exportação realizada com sucesso")
        self.msgBox.setWindowTitle("Mensagem")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec()
        
    def deletar(self):
        self.caminho = ""
        self.quit_msg = "Você tem certeza que deseja apagar todos os códigos do banco de dados"
        self.reply = QMessageBox.question(self, 'Messagem', 
                                           self.quit_msg, QMessageBox.Yes, QMessageBox.No)
        
        #Se confirmar o desejo de fechar...
        if self.reply == QMessageBox.Yes:
            
            self.base = atualizar_bd_produtos(self.caminho)
            self.base.apagar_produtos()
            
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Banco de dados apagado com sucesso")
            self.msgBox.setWindowTitle("Mensagem")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.exec()

#Definição da janela
class Window_caminho_base_xml(QWidget):
    def __init__(self,parent=None):
        super(Window_caminho_base_xml, self).__init__(parent)
        
        #Configuração da janela
        self.setWindowTitle("Base de xml's")
        self.setGeometry(200, 300, 300, 160)
       
        #Criação dos campos
        self.qline_caminho_base = QLineEdit()
        self.btn_caminho_base  = QPushButton("Selecionar")
    
        self.qline_caminho_fonte = QLineEdit()
        self.btn_caminho_fonte  = QPushButton("Selecionar")
        
        #Conexão dos botões
        # self.btn_caminho_base.clicked.connect(self.selecionar_caminho_base)
        self.btn_caminho_fonte.clicked.connect(self.selecionar_caminho_fonte)
                
        #Exibir o layout
        self.exibir_layout = self.layout()
        
    def layout(self):
        
        #Adicionar os itens no groupbox1
        layout1 = QHBoxLayout()
        layout1.addWidget(self.qline_caminho_base)
        layout1.addWidget(self.btn_caminho_base)
        layout1.addStretch(1)

        #Configurar o groupbox
        groupBox1 = QGroupBox("Selecione a base para arquivar XML's analisados")
        groupBox1.setLayout(layout1)
        
        #Adicionar os itens no groupbox2
        layout2 = QHBoxLayout()
        layout2.addWidget(self.qline_caminho_fonte)
        layout2.addWidget(self.btn_caminho_fonte)
        layout2.addStretch(1)
        
        #Configurar o groupbox
        groupBox2 = QGroupBox("Selecione o diretório com a fonte de XML's")
        groupBox2.setLayout(layout2)

        #Adicionar itens no layout da janela
        layout_final = QVBoxLayout()
        layout_final.addWidget(groupBox1)
        layout_final.addWidget(groupBox2)
        
        #Ativar layout
        self.setLayout(layout_final)
        
    # def selecionar_caminho_base(self):
                
    #     # self.file = QFileDialog.getOpenFileName(self, "Selecione o arquivo")
    #     # self.qline_caminho_base.setText(self.file[0])
        
    def selecionar_caminho_fonte(self):
        
        self.file = QFileDialog.getExistingDirectory(self, "Selecione o arquivo")
        self.qline_caminho_fonte.setText(self.file)
        self.base = atualizar_bd_fonte_xml(self.file)
        self.base.atualizar()
            

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=Window()
    form.show()
    sys.exit(app.exec_())
    