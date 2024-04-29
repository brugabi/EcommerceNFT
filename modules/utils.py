from datetime import datetime

def agora():
    '''
    '''
    return datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

def log(msg:str):
    print(f"[{agora()}]",msg,sep=" ")