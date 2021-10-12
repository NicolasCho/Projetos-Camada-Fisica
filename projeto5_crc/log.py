from datetime import datetime
from sys import byteorder
#https://docs.python.org/3/library/datetime.html
#https://www.programiz.com/python-programming/datetime/current-datetime - pegar data e horário atual

def write_line(msg_type, get_or_send, n_bytes, pckg_n = 0, n_of_pckgs = 0, crc = 0):
    """
        Escreve uma linha no log correspondente 
    """
    current_datetime = datetime.now()
    crc = crc.to_bytes(2, byteorder='big')
    dt_string = current_datetime.strftime('%d/%m/%Y %H:%M:%S')  #string da data e horário

    if msg_type == 3:
        log_line = dt_string + ' / ' + get_or_send + ' / ' + str(msg_type) + ' / ' + str(n_bytes) + ' / ' + str(pckg_n) + ' / ' + str(n_of_pckgs) + ' / ' + str(crc) + '\n'
    else:
        log_line = dt_string + ' / ' + get_or_send + ' / ' + str(msg_type) + ' / ' + str(n_bytes) + '\n'

    return log_line


def client_write_on_file(ts_list, log):
    ts_list.sort()
    if len(ts_list) == 0:
        path = "logs/client1.txt"
    else:
        ts_string = ''
        for ts in ts_list:
            if ts_string == '':
                ts_string += str(ts)
            else:
                ts_string += '_' + str(ts)
        path = 'logs/client{}.txt'.format(ts_string)
    
    with open (path, 'a+') as f:
        f.write(f"{log}")

def server_write_on_file(ts_list, log):
    ts_list.sort()
    if len(ts_list) == 0:
        path = "logs/server1.txt"
    else:
        ts_string = ''
        for ts in ts_list:
            if ts_string == '':
                ts_string += str(ts)
            else:
                ts_string += '_' + str(ts)
        path = 'logs/server{}.txt'.format(ts_string)
    
    with open (path, 'a+') as f:
        f.write(f"{log}")
    



