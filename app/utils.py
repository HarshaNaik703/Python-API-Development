import bcrypt

def hashing(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def rehashing(password_plain:str, password_hashed:str)->bool:
    return bcrypt.checkpw(
        password_plain.encode('utf-8'),
        password_hashed.encode('utf-8')
    )
