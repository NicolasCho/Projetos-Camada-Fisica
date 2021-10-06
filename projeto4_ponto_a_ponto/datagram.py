import math


def dg_head(msg_type, n_of_pckgs = 0, pckg_n = 0, archive_id = 0, payload_size = 0, expected_pckg = 0, last_pckg = 0):
    """
    Recebe o tipo da mensagem, número total de pacotes do arquivo, número do pacote sendo enviado, id do arquivo, tamanho do payload, pacote esperado, ultimo pacote recebido com sucesso.
    Retorna um head de datagrama.

    Tipos de mensagem: 
            1-(cliente) Cliente convidando servidor para transmissão (HANDSHAKE). Deve possuir byte identificador (número do servidor).
                Já deve conter o número total de pacotes que se pretende enviar

            2-(server) Após server receber uma mensagem tipo 1 com o número identificador correto. 
                O significado de uma mensagem tipo 2 é que o servidor está ocioso e, portanto, pronto para receber o envio dos pacotes. 

            3-(cliente) Mensagem de dados. Contém de fato um bloco do dado a ser enviado (payload).
                Essa mensagem deve conter também o número do pacote que envia (começando do 1) e o total de pacotes a serem enviados

            4-(server) Enviada após receber mensagem do tipo 3. Informa que recebeu o pacote correto com eop no local correto. Deve conter o número do último pacote recebido e já aferido.

            5-(cliente/server) Mensagem de time out. Toda vez que o limite de espera exceder o timer dedicado a isso, em qualquer um dos lados, 
                deve-se enviar essa mensagem e finalizar a conexão.

            6-(server) Mensagem de erro, seja por estar com bytes faltando, fora do formato correto ou por não ser o pacote esperado pelo servidor (pacote 
                repetido ou fora da ordem). Deve conter o número correto esperado do pacote no h6, orientando o cliente para reenvio.
    """
    h0 = msg_type.to_bytes(1, byteorder ='big')         # tipo da msg
    h1 = (1).to_bytes(1, byteorder='big')               # id do sensor (1)
    h2 = (2).to_bytes(1, byteorder='big')               # id do server (2)

    h3 = n_of_pckgs.to_bytes(1, byteorder ='big')       # número total de pacotes
    h4 = pckg_n.to_bytes(1, byteorder ='big')           # número do pacote sendo enviado
    if msg_type == 1:                           
        h5 = archive_id.to_bytes(1, byteorder ='big')   # id do arquivo se for handshake
    else:
        h5 = payload_size.to_bytes(1, byteorder ='big') # tamanho do payload se for dados
    h6 = expected_pckg.to_bytes(1, byteorder ='big')    # pacote solicitado para recomeço quando erro no envio
    h7 = last_pckg.to_bytes(1, byteorder ='big')        # último pacote recebido com sucesso

    h8h9 = (0).to_bytes(2, byteorder='big')             # CRC (não implementado)

    return h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8h9

def datagram(head, eop, payload=None):
    """
    Recebe o head, payload e eop (todos em byte) e devolve o datagrama correspondente.
    """
    if payload is None:
        return head + eop
    else:
        return head + payload + eop
    
def get_n_of_pckgs(message):
    """
        Retorna o número de pacotes da mensagem a ser enviada
    """
    return math.ceil(len(message)/114)
        
def create_pckg(message, pckg_no, n_of_pckgs, error = False):
    """
        Cria o pacote com base em seu número
    """
    eop = (2145369870).to_bytes(4, byteorder='big')
    start = 114 * (pckg_no - 1)

    if pckg_no != n_of_pckgs:
        end = start + 114
        payload = message[start:end]
        payload_size = len(payload)
    else:
        payload = message[start:]
        payload_size = len(payload)

    if error:
        pckg_no = pckg_no - 1 
        
    head = dg_head(msg_type=3, n_of_pckgs=n_of_pckgs, pckg_n=pckg_no, payload_size=payload_size)

    dg = datagram(head, eop, payload = payload)

    return dg
