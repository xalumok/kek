import requests
import json
import time
import random
import codecs
TOKEN = "700433018:AAEYDasuKqpKutWqwRgKDJVPzF2RwBMS9K4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

moskal = codecs.open("phrases/moskal_phrases.txt","r", "utf-8").readlines()
for i in range(len(moskal)):
    moskal[i]=moskal[i][:-2]
layka_na_moskalya = codecs.open("phrases/laika_na_moskala.txt", "r", "utf-8").readlines()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text():
    updates = get_updates()
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def reply_message(text, chat_id, msg_id):
    url = URL + "sendMessage?text={}&chat_id={}&reply_to_message_id={}".format(text, chat_id, msg_id)
    get_url(url)

def get_layka_on_moskal():
    return layka_na_moskalya[random.randint(0, len(layka_na_moskalya)-1)]

lastMsgId=1

def set_last_msg():
    updates = get_updates()
    num_updates = len(updates["result"])
    updates = updates["result"]
    global lastMsgId
    lastMsgId = updates[num_updates-1]["message"]["message_id"]

def check_on_moskal(msg):
    ok = False
    for slovo in moskal:
        if slovo in msg.lower():
            ok = True
    return ok



def analize():
    updates = get_updates()
    num_updates = len(updates["result"])
    updates = updates["result"]
    global lastMsgId
    lastMsgId1 = lastMsgId
    for i in range(min(lastMsgId1, num_updates-5), num_updates):
        # print(updates[i])
        try:
            msg = updates[i]["message"]["text"]
            name = updates[i]["message"]["from"]["first_name"]
            chat_id = updates[i]["message"]["chat"]["id"]
            message_id = updates[i]["message"]["message_id"]
            if (message_id <= lastMsgId):
                continue
            lastMsgId1 = message_id
            if (check_on_moskal(msg)):
                reply_message(get_layka_on_moskal().format(name), chat_id, message_id)
        except:
            print("No text exception")
    lastMsgId = lastMsgId1


def main():
    set_last_msg()
    while True:
        analize()

        time.sleep(0.4)


if __name__ == '__main__':
    main()