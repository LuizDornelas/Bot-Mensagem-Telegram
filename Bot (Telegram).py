# importar biblioteca para requisições http
import requests
from imap_tools import MailBox, AND
import datetime

# Retorna o id do último grupo onde o bot foi adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": msg}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

# token único utilizado para manipular o bot (não deve ser compartilhado), token é criado pelo BotFather
token = ''

# id do chat que será enviado as mensagens
chat_id_test = 1

#print(last_chat_id(token))

# pegar emails de um remetente para um destinatário
username = ""
password = ""

# lista de imaps: https://www.systoolsgroup.com/imap/
meu_email = MailBox('imap.gmail.com').login(username, password)

msg = ""

# criterios: https://github.com/ikvk/imap_tools#search-criteria Limite de um e-mail, sendo o mais recente com um determinado título
for email in meu_email.fetch(AND(subject=""), limit=1, reverse=True):        
    msg = email.text
    

if msg != "":
    #Tratamento da mensagem e delta o e-mail onde encontrou a mensagem, para caso coloque o bot em loop e não queria que fique spamando mensagem
    msg = "Status arquivo selecionados "+ datetime.date.today().strftime('%d/%m' + ":\n\n" + msg)
    meu_email.delete([msg.uid for msg in meu_email.fetch(AND(subject=""), limit=1, reverse=True)])
    send_message(token, chat_id_test, msg)
