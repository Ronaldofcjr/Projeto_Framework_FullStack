from twilio.rest import Client
from src.Application.Service.user_service import UserService


class WhatsAppService:

    @staticmethod
    def enviar_codigo(numero, token):
        
        account_sid = 'SUA_ACCOUNT_SID'
        auth_token = 'SUA_AUTH_TOKEN'

        cliente = Client(account_sid, auth_token)

        mensagem = f"Seu código de verificação é: {token}"

        cliente.messages.create(
            from_='whatsapp:+14155238886',
            body=mensagem,
            to=f'whatsapp:{numero}'
        )