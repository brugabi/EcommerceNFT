from datetime import datetime

def agora():
    '''
    '''
    return datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

def log(msg:str):
    print(f"[{agora()}]",msg,sep=" ")

def compress_lzw(uncompressed):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    
    # Convert the list of codes to bytes
    byte_array = bytearray()
    for code in result:
        byte_array.extend(code.to_bytes((code.bit_length() + 7) // 8, byteorder='big'))
    
    return byte_array

def decompress_lzw(compressed):
    from io import BytesIO
    
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    result = BytesIO()
    
    compressed_codes = []
    buffer = 0
    bits_left = 0
    
    for byte in compressed:
        buffer = (buffer << 8) | byte
        bits_left += 8
        
        while bits_left >= 9:
            bits_left -= 9
            code = (buffer >> bits_left) & 0x1FF  # 0x1FF is 9 bits mask
            compressed_codes.append(code)
    
    w = chr(compressed_codes.pop(0))
    result.write(w.encode())
    
    for k in compressed_codes:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        
        result.write(entry.encode())
        
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        
        w = entry
    
    return result.getvalue().decode()
