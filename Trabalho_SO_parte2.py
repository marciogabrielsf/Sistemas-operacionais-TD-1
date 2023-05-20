from multiprocessing import Process, Array, Queue, Lock
from os import system


def readFile(filename): #função que lê o arquivo (apenas para refatoração)
    with open(filename, mode='rb') as file_obj: #lê o arquivo em modo "rb" (binário)
        name = file_obj.name
        content = file_obj.read()
        return content, name




def process1(shm , queue_processo_1: Queue, lock):
    while True:
        #receive
        
        with lock: #trava o mutex
            if(shm.value != b''): #caso a shm seja diferente de vazia
                    print(" Processo 1 - Recebeu:", shm.value.decode()) #printa o conteudo do arquivo decodado
                    shm.value = b'' #torna a shm vazia novamente.

            # send   

            if(not queue_processo_1.empty()):
                  terminalMessage1 = queue_processo_1.get() 
                  if(terminalMessage1):
                      try:
                          content = readFile(terminalMessage1) #le o arquivo usando uma função la em cima, que retorna o conteudo do arquivo em binário
                          shm.value = content[0]; #seta na shm o retorno do "content" que a função readFile retorna.
                          print(' Processo 1 - Enviou:', content[1]) #printa o "name" que a função readFile retorna.
                      except FileNotFoundError: #tratamento de erros
                          print('Diretório invalido.')
                      except Exception as err:
                          print(err)
    

def process2(shm , queue_processo_2: Queue, lock):
    while True:
        #receive
        with lock: #trava o mutex
            if(shm.value != b''): #caso a shm seja diferente de vazia
                    print(" Processo 2 - Recebeu:", shm.value.decode()) #printa o conteudo do arquivo decodado
                    shm.value = b'' #torna a shm vazia novamente.        
            # send   

            if(not queue_processo_2.empty()):
                     terminalMessage1 = queue_processo_2.get() 
                     if(terminalMessage1):

                         try:
                             content = readFile(terminalMessage1) #le o arquivo usando uma função la em cima, que retorna o conteudo do arquivo em binário
                             shm.value = content[0]; #seta na shm o retorno do "content" que a função readFile retorna.
                             print(' Processo 2 - Enviou:', content[1]) #printa o "name" que a função readFile retorna.
                         except FileNotFoundError: #tratamento de erros
                             print('Diretório invalido.')
                         except Exception as err:
                             print(err)

if __name__ == '__main__':
    # create shared memory
    shm = Array('c',2048,  lock=True)
    
    
    queue_processo_1 = Queue() #cria a fila para integrar o terminal com o processo 1.
    queue_processo_2 = Queue() #cria a fila para integrar o terminal com o processo 2.

    lock = Lock() #cria o mutex

    p1 = Process(target=process1, args=(shm, queue_processo_1, lock)) #cria o processo 1
    p2 = Process(target=process2, args=(shm, queue_processo_2, lock)) #cria o processo 2

    p1.start() #inicia o processo 1
    p2.start()# inicia o processo 2 
    
    system('cls') #limpa a tela
    while(True):

        print('Qual processo voce deseja Selecionar? \n 1- Processo 1 \n 2- Processo 2 \n 0- Fechar')
        option = input()
        match option: #switch case para o menu
            case '1':
                system('cls')
                print('Digite o Diretório do arquivo para mandar para o processo 2:')
                message1 = input() #pega o input do usuário
                system('cls')
                queue_processo_1.put(message1) #coloca o que o user digitou na fila para ser lido lá no processo
                
            case '2':
                system('cls')
                print('Digite o Diretório do arquivo para mandar para o processo 1')
                message2 = input()
                system('cls')
                queue_processo_2.put(message2) #coloca o que o user digitou na fila para ser lido lá no processo
            case '0':
                break
                
            case _:
                system('cls')
                print('- digita algo que preste seu inutil')
                
                


    # finalizar os dois processos
    p1.terminate()
    p2.terminate()

    # limpar a shared memory
    shm.value = b''