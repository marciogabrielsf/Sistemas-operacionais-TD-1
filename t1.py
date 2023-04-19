import multiprocessing
from time import sleep

def processo1(texto, queue_enviar, queue_receber):
    while True:
        queue_enviar.put(texto)
        print(f'Mensagem enviada - P1: {texto}')
        sleep(3)
        resposta = queue_receber.get()
        print(f'Resposta recebida - P1: {resposta}')
        sleep(3)

def processo2(texto, queue_receber, queue_enviar):
    while True:
        queue_enviar.put(texto)
        print(f'Mensagem enviada - P2: {texto}')
        sleep(3)
        mensagem = queue_receber.get()
        print(f'Resposta recebida - P2: {mensagem}')
        sleep(3)

if __name__ == '__main__':
    queue_enviar_1 = multiprocessing.Queue()
    queue_receber_1 = multiprocessing.Queue()
    queue_enviar_2 = multiprocessing.Queue()
    queue_receber_2 = multiprocessing.Queue()
    
    texto1 = 'Mensagem da P1 (texto 1)'
    texto2 = 'Mensagem da P2 (texto 2)'

    p1 = multiprocessing.Process(target=processo1, args=(texto1, queue_enviar_1, queue_receber_2))
    p2 = multiprocessing.Process(target=processo2, args=(texto2, queue_enviar_1, queue_receber_2))

    p1.start()
    p2.start()

    # p1.join()
    # p2.join()