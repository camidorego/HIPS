import hashlib
def calcular_hash(path_archivo):
    hash=hashlib.sha256() # creamos el objeto sha256
    with open(path_archivo, "rb") as f:
    # se genera el hash de todas las lineas concatenadas del archivo 
        while True:
            info=f.read(65536)
            if not info:
                break
            hash.update(info)
        return hash.hexdigest()