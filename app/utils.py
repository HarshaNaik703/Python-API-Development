from fastapi import HTTPException, status
import bcrypt

def hashing(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def rehashing(password_plain:str, password_hashed:str)->bool:
    return bcrypt.checkpw(
        password_plain.encode('utf-8'),
        password_hashed.encode('utf-8')
    )


def password_check(newpass, password):
    old_password = rehashing(newpass, password)
    if old_password:
        print(f"You are trying to update same password, try new one")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="New password cannot be the same as old password")

if __name__ == "__main__":
    str1 = hashing("harsha")
    str2 = hashing("harsha")
    print(str1)
    print(str2)
    print(str1==str2)
