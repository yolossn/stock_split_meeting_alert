from cryptography.fernet import Fernet
import os
def getKeys():
    key=os.environ.get("key",None)
    eid=os.environ.get("eid",None)
    pwd=os.environ.get("pwd",None)
    if key and eid and pwd:
        ciph=Fernet(str.encode(key))
        eid=ciph.decrypt(str.encode(eid))
        pwd=ciph.decrypt(str.encode(pwd))
    return eid.decode(),pwd.decode()


