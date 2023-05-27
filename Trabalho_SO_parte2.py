'''bibliotecas usadas para manipulação dos processos, shm e mutex'''
from multiprocessing import shared_memory, Lock
from os import system
import multiprocessing


def readFile(filename):
    '''função que pega o conteudo do arquivo e retorna em bytes'''
    with open(filename, mode='rb') as file_obj: 
        conteudo = file_obj.read() 
        return conteudo



def processo1_send(filename, lock):

        '''Função processo 1 envia:
           Recebe o arquivo e converte em bytes;
           acessa a memoria compartilhada pelo nome; 
           copia o conteudo do arquivo para a memória compartilhada;
           fecha a memoria compartilhada;
           bloqueia p/ garantir a exclusão mutua.'''

        lock.acquire()
        conteudo = readFile(filename)
        

        shmm = shared_memory.SharedMemory('s')
        
        conteudo_bytes = (len(conteudo)+4).to_bytes(4, 'little') 
        
        buffer = conteudo_bytes + conteudo
        shmm.buf[:len(conteudo) + len(conteudo_bytes)] = buffer
        
        print("arquivo enviado para Ana!")
        shmm.close()
        
       


def processo1_receive(lock):
    
        '''Função em que o processo 1 recebe: 
            Acessa a memoria compartilhada pelo nome;
            percorre a memoria e copia o conteudo até chegar em '\0' e parar a leitura;
            pega o conteudo do buf da memoria e copia para variável conteudo;
            escreve o conteúdo copiado da memoria para dentro do arquivo. '''
     

        
        shmm = shared_memory.SharedMemory('s')

        conteudo_length = int.from_bytes(bytes(shmm.buf[:4]), 'little')
             
        conteudo = bytes(shmm.buf[4:conteudo_length])

        arquivo = open('recebido.jpg', 'wb')
        arquivo.write(conteudo)
        print('Pedro Recebeu: ', conteudo)

        lock.release()
        arquivo.close()
        shmm.close()
       



def processo2_send(filename, lock):

        '''função em que o processo 2 envia:
           Função que recebe o arquivo e converte em bytes;
           acessa a memoria compartilhada pelo nome; 
           copia o conteudo do arquivo para a memória compartilhada;
           fecha a memoria compartilhada;
           bloqueia p/ garantir a exclusão mutua.'''
        
        
        lock.acquire()
        conteudo = readFile(filename)

        shmm = shared_memory.SharedMemory('s')

        conteudo_bytes = (len(conteudo)+4).to_bytes(4, 'little') 
        
        buffer = conteudo_bytes + conteudo
        shmm.buf[:len(conteudo) + len(conteudo_bytes)] = buffer
        print("arquivo enviado para Pedro!")
        
        shmm.close()
        
        




def processo2_receive(lock):

        '''Função onde o processo 2 recebe: 
            Acessa a memoria compartilhada pelo nome;
            percorre a memoria e copia o conteudo até chegar em '\0' e parar a leitura;
            pega o conteudo do buf da memoria e copia para variável conteudo;
            escreve o conteúdo copiado da memoria para dentro do arquivo. '''
        
        lock.release()
        shmm = shared_memory.SharedMemory('s')
        
        conteudo_length = int.from_bytes(bytes(shmm.buf[:4]), 'little')
             
        conteudo = bytes(shmm.buf[4:conteudo_length])
      
        arquivo = open('recebido.jpg', 'wb')
        arquivo.write(conteudo)
        print('Ana recebeu: ', conteudo)

        
        
        # arquivo.close()
        shmm.close()

        
       

def taskTwoMenu():

        '''Cria a memoria compartilhada;
        '''
        shm = shared_memory.SharedMemory(name='s', create=True, size=2048)
        lock = Lock()
        ''' Executa o loop para decidir quem vai enviar a mensagem '''
        
        while(True):

          print("Quem vai realizar o envio: \n 1- Pedro \n 2- Ana \n 0 - Sair")
          in_process = input()

         
          match in_process: 
            case '1':
              system('cls')
              print("Digite o nome do arquivo e sua extensão: ")
              arq = input()
              system('cls')
          
              p1 = multiprocessing.Process(target=processo1_send, args=(arq, lock,))
              p2 = multiprocessing.Process(target=processo2_receive, args=(lock,))

              p1.start()
              p2.start()
              
              '''sicroniza a execução dos processos'''
              p1.join()
              p2.join()

              # system('cls')

              break

            case '2':
              system('cls')
              print("Digite o nome do arquivo e sua extensão: ")
              arq_2 = input()
              p2 = multiprocessing.Process(target=processo2_send, args=(arq_2, lock))
              p1 = multiprocessing.Process(target=processo1_receive, args=(lock,))
              system('cls')
              p2.start()
              p1.start()

              '''sicroniza a execução dos processos'''
              p2.join()
              p1.join()

              # system('cls')

              break
            case '0':
              break
           
            case _:
              system('cls')
              print("Selecione um valor válido! ")


          shm.close()

       
