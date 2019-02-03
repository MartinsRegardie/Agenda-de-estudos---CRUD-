# Programa: Controle de estudos
# Autor: Rafael Martins Bastos
# Email: rafagha@gmail.com
# Data: 29/01/2019
"""
Esse programa tem o objetivo de salvar oque foi estudado para o autor ter uma noção do que ja foi estudado e por quanto
foi estudado.
"""

#Importando as modulos necessarios
from time import sleep
import os, sqlite3

class Estudo():
    """Um CRUD para auxiliar no estudo"""

    def playsound(self):
        """Som de beep"""
        os.system('beep -f %s -l %s' % (3000, 50))

    def loading_inicio(self):
        """loading do programa"""
        string = " > INICIANDO PROGRAMA"
        for i in range(0, 5):
            os.system("clear")
            string += "."
            print("++++++++ GERENCIADOR DE ESTUDOS 1.0 ++++++++")
            print()
            print(string)
            sleep(0.60)
        self.conexao()
    
    def gravar(self):
        """Função que faz a gravação dos dados no banco de dados commit()"""
        r = input("Deseja gravar informações? (S/N): ").lower()

        if r == "s":
            self.banco.commit()
            print("Dados salvos com sucesso.")
            sleep(3)
            os.system("clear")
            

        elif r == "n":
            print("Dados não salvos")
            sleep(3)
            os.system("clear")
            
        
        else:
            print("Favor digite valor valido")
            self.gravar()
        
        self.menu()


    def conexao(self):
        self.banco = sqlite3.connect("banco")
        self.cursor = self.banco.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MATERIA TEXT NOT NULL,
            PERIODO TEXT NOT NULL,
            HORAS INTEGER NOT NULL
        );
        """)
        print(" > CONECTANDO AO BANCO DE DADOS")
        sleep(2)
        print(" > BANCO DE DADOS CONECTADO COM SUCESSO")
        sleep(2)
        print()
        print("---------------------------------------------")
        input("TECLE QUALQUER TECLA PARA ENTRAR NO MENU ")

    def menu(self):
        """Menu principal"""
        
        self.playsound()

        os.system("clear")
        sleep(0.40)
        print("=====MENU PRINCIPAL=====")
        print()
        sleep(0.40)
        print(" 1 > ADICIONAR ENTRADA  ")
        sleep(0.40)
        print(" 2 > ATUALIZAR ENTRADA  ")
        sleep(0.40)
        print(" 3 > CONSULTAR ENTRADAS ")
        sleep(0.40)
        print(" 4 > DELETAR ENTRADA    ")
        sleep(0.40)
        print(" 5 > SAIR DO PROGRAMA   ")
        sleep(0.40)
        print()
        n = input("Escolha uma opção: ")

        if n == "1":
            self.adicionar()

        elif n == "2":
            self.atualizar()
        
        elif n == "3":
            self.consultar()

        elif n == "4":
            self.deletar()
        
        elif n == "5":
            self.sair()
        
        else:
            os.system("clear")
            print("Favor informe uma opção valida.")
            sleep(3)
            self.menu()

    def adicionar(self):
        """Função que adiciona informações no DB"""
        os.system("clear")
        print("++++++ 1 > ADCIONAR ENTRADA ++++++")
        materia = input("Informe a diciplina que foi estudada: ")
        periodo = input("Informe dia e horario: ")
        horas = float(input("Informe a quantidade de horas estudadas: "))

        self.cursor.execute("""
        INSERT INTO estudo (MATERIA, PERIODO, HORAS) VALUES (?,?,?) """, (materia, periodo, horas))

        self.gravar() 
    
    def atualizar(self):
        """Função que atualiza os dados da tabela"""
        id = input("Informe o ID que deseja alterar/atualizar ou digite 0(zero) para consultar o banco de dados: ")

        if id == "0":
            self.consultar()
            self.atualizar()
        else:
            self.cursor.execute("""
            SELECT * FROM estudo WHERE ID = ?
            """, (id))
            os.system("clear")
            print("=" * 65)
            print("{:<3} {:<25} {:<25} {:<5}".format("ID","MATERIAL","PERIODO","HORAS"))
            print("=" * 65)
            
            for i in self.cursor.fetchall():
                print("{:<3} {:<25} {:<25} {:<5d}".format(i[0],i[1],i[2],i[3]))
            
            print()
            materia = input("Informe a diciplina que foi estudada: ")
            periodo = input("Informe dia e horario: ")
            horas = float(input("Informe a quantidade de horas estudadas: "))
            self.cursor.execute("""
            UPDATE estudo SET 
                MATERIA = ?,
                PERIODO = ?,
                HORAS = ?
            WHERE ID = ? """, (materia, periodo, horas, id))
            self.gravar()

    def consultar(self):
        """função que exibe os dados contidos no banco de dados"""
        self.cursor.execute("""
        SELECT * FROM estudo;
        """)
        os.system("clear")
        sleep(0.50)
        print("=" * 65)
        print("{:<3} {:<25} {:<25} {:<5}".format("ID","MATERIAL","PERIODO","HORAS"))
        print("=" * 65)
        horas = 0
        for i in self.cursor.fetchall():
            sleep(0.50)
            print("{:<3} {:<25} {:<25} {:<5d}".format(i[0],i[1],i[2],i[3]))
            horas += i[3]
        print()
        self.cursor.execute("SELECT COUNT(*) FROM estudo")
        linha = self.cursor.fetchone()
        print("Quantidade de entradas: {}".format(linha[0]))
        print("Total de Horas Estudadas:", horas)
        print("=" * 65)
        input("Pressione qualquer tecla para voltar ao menu principal")
        self.menu()
    
    def deletar(self):
        """Função que deleta dados da tabela"""
        id = input("Informe o ID que deseja deletar ou 0(zero) para consultar o bd: ")

        if id == "0":
            self.consultar()
            
        else:
            self.cursor.execute("""
            SELECT * FROM estudo WHERE ID = ?
            """, (id))
            os.system("clear")
            print("=" * 65)
            print("{:<3} {:<25} {:<25} {:<5}".format("ID","MATERIAL","PERIODO","HORAS"))
            print("=" * 65)
            
            for i in self.cursor.fetchall():
                print("{:<3} {:<25} {:<25} {:<5d}".format(i[0],i[1],i[2],i[3]))
            
            print()
            self.cursor.execute("""
            DELETE FROM estudo WHERE ID = ?
            """, (id))
            self.gravar()


    def sair(self):
        self.banco.close()
        os.system("clear")
        print("Finalizando o programa.")
        sleep(3)
        self.playsound()
        os.system("clear")
        os.system("exit")






a = Estudo()
a.loading_inicio()
a.menu()
