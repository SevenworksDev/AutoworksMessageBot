import requests
import base64
import itertools
import threading
import string
import time

accountid = ""
password = ""

headers = {"User-Agent": ""}

def xor(data, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, itertools.cycle(key)))

def base64_encode(string: str) -> str:
    return base64.urlsafe_b64encode(string.encode()).decode()

def base64_decode(string: str) -> str:
    return base64.urlsafe_b64decode(string.encode()).decode()

def gjp_encrypt(data):
    return base64.b64encode(xor(data, "37526").encode()).decode()

def message_encode(data):
    return base64_encode(xor(data, '14251'))

def message_decode(data):
    return base64_encode(xor(data, '14251'))

def getFriendRequest():
    data = {
        "accountID": accountid,
        "gjp": gjp_encrypt(password),
        "page": "0",
        "secret": "Wmfd2893gb7"
    }
    try:
        r = requests.post("http://www.boomlings.com/database/getGJFriendRequests20.php", data=data, headers=headers).text
        targetAcc = r.split(":")[15]
        targetReqID = r.split(":")[17]
        return targetAcc, targetReqID
    except Exception:
        return None, None

def acceptFriendRequest():
    targetAcc, targetReqID = getFriendRequest()
    if targetAcc is not None and targetReqID is not None:
        data = {
            "accountID": accountid,
            "targetAccountID": targetAcc,
            "requestID": targetReqID,
            "gjp": gjp_encrypt(password),
            "secret": "Wmfd2893gb7"
        }
        try:
            requests.post("http://www.boomlings.com/database/acceptGJFriendRequest20.php", data=data, headers=headers).text
        except Exception:
            return None

def getMessage():
    data = {
        "accountID": accountid,
        "gjp": gjp_encrypt(password),
        "secret": "Wmfd2893gb7"
    }
    try:
        r = requests.post("http://www.boomlings.com/database/getGJMessages20.php", data=data, headers=headers).text
        
        targetAcc = r.split(":")[5]
        messageID = r.split(":")[7]

        data = {
            "accountID": accountid,
            "gjp": gjp_encrypt(password),
            "messageID": messageID,
            "secret": "Wmfd2893gb7"
        }
        rr = requests.post("http://www.boomlings.com/database/downloadGJMessage20.php", data=data, headers=headers).text
        user = rr.split(":")[1]
        tsubject = base64_decode(rr.split(":")[9])
        tbody = message_decode(rr.split(":")[15])
        targetAcc = rr.split(":")[5]
        messageID = rr.split(":")[7]
        return user, tsubject, tbody, targetAcc, messageID
    except Exception:
        return None, None, None, None, None


def deleteMessage(target):
    data = {
        "accountID": accountid,
        "gjp": gjp_encrypt(password),
        "messageID": target,
        "secret": "Wmfd2893gb7"
    }
    try:
        requests.post("http://www.boomlings.com/database/deleteGJMessages20.php", data=data, headers=headers).text
    except Exception:
        return None

def uploadMessage(subject, body):
    user, tsubject, tbody, targetAcc, messageID = getMessage()
    deleteMessage(messageID)
    data={
        "accountID": accountid,
        "gjp": gjp_encrypt(password),
        "toAccountID": targetAcc,
        "subject": base64_encode(subject),
        "body": message_encode(body),
        "secret": "Wmfd2893gb7",
    }
    try:
        requests.post("http://www.boomlings.com/database/uploadGJMessage20.php", data=data, headers=headers).text
    except Exception:
        return None

def bot():
    user, tsubject, tbody, targetAcc, messageID = getMessage()

    if tsubject == "hello":
        uploadMessage(f"[Auto-Responder]: Vacation", f"Hello {user}, I see you have messaged me but I am not currently availible to speak to you right now because I am taking a two week vacation. Talk to you soon!")
    elif tsubject == "hello2":
        pass
    elif tsubject == "hello3":
        pass
    else:
        pass

while True:
    bot()
    time.sleep(10)
