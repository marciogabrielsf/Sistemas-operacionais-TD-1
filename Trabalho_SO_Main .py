from multiprocessing import Array
from Trabalho_SO_parte1 import taskOneMenu
from Trabalho_SO_parte2 import taskTwoMenu
from Trabalho_SO_parte3 import taskThreeMenu
from os import system

def mainMenu():
    while(True):

        print('O que você deseja fazer? \n 1- Enviar texto entre processos \n 2- Enviar Arquivos entre processos \n 3- Enviar uma mensagem para vários \n 0- Fechar')
        option = input()
        match option: #switch case para o menu
            case '1':
                system('cls')
                taskOneMenu()
                
            case '2':
                system('cls')
                taskTwoMenu()
                
            case '3':
                system('cls')
                taskThreeMenu()
            case '0':
                system('cls')
                break
                
            case _:
                system('cls')
                print('- digita algo que preste seu inutil')
                
                

if __name__ == '__main__':
    # inicia o menu principal
    system('cls') #limpa a tela
    mainMenu()
    
    
#n sei se pode separar cada função em cada arquivo, então vai esse com 200 linha mesmo kkkkk (agonia)