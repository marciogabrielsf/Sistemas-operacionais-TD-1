from multiprocessing import Process, Array, Queue
from os import system

def process1(shm, queue_processo_1: Queue):
    # pega o último valor da shared memory. serve para comparar se ela foi alterada.
    lastShmValue = shm.value.decode()
    # inicia um loop entre os processos
    while True:
        
        
        #receive
        
        # fica comparando o valor da shm atual com o último valor alterado da shared memory
        shmActual = shm.value.decode()
        if(lastShmValue != shmActual): #caso detecte que foi alterado, significa que a shm recebeu uma mensagem do outro processo.
            print(" Processo 1 - Recebeu:", shmActual)
            lastShmValue = shmActual
            
        # send   
        
        # checa se a queue não está vazia
        if(not queue_processo_1.empty()):
            terminalMessage1 = queue_processo_1.get() #pega o que tem na fila
            if(terminalMessage1): #if pra evitar erros.
                shm.value = terminalMessage1.encode(); #pega o que estava na fila (que foi recebido do terminal), encoda em bytecode e coloca na shm.
                print(' Processo 1 - Enviou:', terminalMessage1) #print para avisar que o processo colocou uma mensagem na shm
                lastShmValue = terminalMessage1 #reseta o último valor da shm.
    

def process2(shm, queue_processo_2: Queue):
    # pega o último valor da shared memory. serve para comparar se ela foi alterada.
    lastShmValue = shm.value.decode()
    # fica comparando o valor da shm atual com o último valor alterado da shared memory
    while True:
        #receive
        shmActual = shm.value.decode()
        #caso detecte que foi alterado, significa que a shm recebeu uma mensagem do outro processo.
        if(lastShmValue != shmActual):
            print(" Processo 2 - Recebeu:", shmActual)
            lastShmValue = shmActual
            
        # send   

        
        # checa se a queue não está vazia
        if(not queue_processo_2.empty()):
            terminalMessage2 = queue_processo_2.get()
            if(terminalMessage2): #if pra evitar erros.
                shm.value = terminalMessage2.encode(); #pega o que estava na fila (que foi recebido do terminal), encoda em bytecode e coloca na shm.
                print(' Processo 2 - Enviou:', terminalMessage2) #print para avisar que o processo colocou uma mensagem na shm
                lastShmValue = terminalMessage2 #reseta o último valor da shm.
    

if __name__ == '__main__':
    # create shared memory
    shm = Array('c',2048,  lock=True)
    
    #fila para fazer a comunicação entre o terminal principal e os processos
    queue_processo_1 = Queue()
    queue_processo_2 = Queue()



    # criar os dois processos com os devidos parâmetros (shared memory, fila de input do usuário)
    p1 = Process(target=process1, args=(shm, queue_processo_1))
    p2 = Process(target=process2, args=(shm, queue_processo_2))

    # iniciar os dois processos
    p1.start()
    p2.start()
    
    # iniciar o menu principal
    system('cls') #limpa a tela
    while(True):

        print('Qual processo voce deseja Selecionar? \n 1- Processo 1 \n 2- Processo 2 \n 0- Fechar')
        option = input()
        match option: #switch case para o menu
            case '1':
                system('cls')
                print('Digite sua mensagem para o Processo 2')
                message1 = input() #pega o input do usuário
                system('cls')
                queue_processo_1.put(message1) #coloca o que o user digitou na fila para ser lido lá no processo
                
            case '2':
                system('cls')
                print('Digite sua mensagem para o Processo 1')
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