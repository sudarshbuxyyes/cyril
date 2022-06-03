from email import message
import requests
class Messenger():
    def __init__(self):
        print("Messenger initialised")
        self.bot_token = "5486965574:AAF4a-22us68EJdgfqXTT_mp87LlX3jo0cc"
        self.chatID = self.get_chatID()
        pass
    def get_chatID(self):
        print("Getting chatID")
        chatID = "chat_id"
        get_chatID = 'https://api.telegram.org/bot' + self.bot_token + '/getUpdates'
        response = requests.get(get_chatID)
        chatID = response.json()['result'][0]['message']['from']['id']
        return chatID
    def send_message(self, message):
        print("Sending message: " + message)
        # r = requests.post("http://localhost:5000/message", data={"message": message})
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + str(self.chatID) + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
        return response.json()