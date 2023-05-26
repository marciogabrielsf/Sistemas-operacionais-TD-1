import multiprocessing

def processo_filho(processo_id, shm, num_processos, barreira):
    print(f"processo filho {processo_id} iniciado")
    barreira.wait()  # Aguarda a barreira para sincronizar a inicialização dos processos filhos

    for i in range(num_processos):
        mensagem = shm.get()
        if mensagem:
            print(f"processo filho {processo_id} recebeu a mensagem: {mensagem}")
            shm.task_done()
            break
        
def processo_sender(shm, num_processos, commQueue: multiprocessing.Queue):
    print("processo pai iniciado \n")
    message = commQueue.get()
    for i in range(num_processos):
        shm.put(message)
    print("processo pai finalizado. \n")

def taskThreeMenu():
    while True:
            num_processos = int(input('Digite quantos processos você quer: '))
            if num_processos <= 2:
                print('digite um numero maior doq 2 mah')
            else:
                break

    # Cria a fila compartilhada para a troca de mensagens
    shm = multiprocessing.JoinableQueue()
    
    #Fila para comunicação entre o codigo e o processo
    commQueue = multiprocessing.Queue()

    # Cria a barreira para sincronizar a inicialização dos processos filhos
    barreira = multiprocessing.Barrier(num_processos)

    # Cria os processos filhos
    processos: list[multiprocessing.Process] = []
    for i in range(num_processos):
        p = multiprocessing.Process(target=processo_filho, args=(i, shm, num_processos, barreira))
        p.start()
        processos.append(p)
    
    #coloca a mensagem na queue para integrar o terminal com o processo
    mensagem = input("qual a mensagem que vc quer enviar \n")
    commQueue.put(mensagem)
    #inicia o processo enviador
    sender = multiprocessing.Process(target=processo_sender, args=(shm, num_processos, commQueue))
    sender.start()
    sender.join()
        
    for processo in processos:
        processo.join()
        processo.close()
    print('Todos os processos leram, fechando a shm. \n')
    shm.close()
