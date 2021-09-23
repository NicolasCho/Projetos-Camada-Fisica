import math


def dg_head(status, n_of_pckgs, pckg_n, payload_size):
    """
    Recebe o status/ação da mensagem (1 byte), a quantidade de pacotes(3 bytes), o número do pacote(3 bytes) e o tamanho do payload (3 bytes) 
    e devolve o head do datagrama composto por estes elementos (em bytes)

    Status: 
            1-(cliente)Dados enviados pelo cliente
            2-(server)Mensagem foi recebida com sucesso, enviar novo pacote
            3-(server)Erro de transmissão, reenviar o pacote
    """
    return status + n_of_pckgs + pckg_n + payload_size

def datagram(head, eop, payload=None):
    """
    Recebe o head, payload e eop (todos em byte) e devolve o datagrama correspondente.
    """
    if payload is None:
        return head + eop
    else:
        return head + payload + eop

def dg_fragmentation(message, pckg_n_error = False, payload_error = False):
    """
    Recebe a mensagem (em bytes) a ser fragmentada e devolve a lista de todos os pacotes (estruturados em datagramas) 
    que formam a imagem.
    Considera-se payload com tamanho máximo de 114 bytes
    A função também recebe argumentos adicionais para simular erros na comunicação
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    datagrams = []
    n_of_pckgs = math.ceil(len(message)/114)
    n_of_pckgs_bytes = n_of_pckgs.to_bytes(3, byteorder='big')

    status = (1).to_bytes(1, byteorder='big')
    start = 0
    end = 114

    pckg_n = 1
    for pckg in range(0, n_of_pckgs):
        if start + 114 <= len(message):
            payload = message[start:end]
            payload_size_bytes = (len(payload)).to_bytes(3, byteorder='big')
            start += 114
            end += 114
        else:
            payload = message[start:]
            payload_size_bytes = (len(payload)).to_bytes(3, byteorder='big')
        
        pckg_n_bytes = pckg_n.to_bytes(3, byteorder='big')

        #Adiciona 5 bytes extras no payload do pacote 5, posicionando assim o eop no local errado 
        if payload_error and pckg_n == 5:
            extra_bytes = (1122).to_bytes(5, byteorder='big')
            payload += extra_bytes

        head = dg_head(status, n_of_pckgs_bytes, pckg_n_bytes, payload_size_bytes)

        dg = datagram(head, eop, payload = payload)
        datagrams.append(dg)

        #Pula o pacote 6, criando erro na comunicação
        if pckg_n_error and pckg_n == 5:
            pckg_n +=1

        pckg_n += 1

    return datagrams

    


        
