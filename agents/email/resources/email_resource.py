from agents.email.auth.email_auth import authenticate_gmail
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from models.AgentResponseModel import ResponseModel


def list_emails_tool() -> ResponseModel:
    """
    Lista os 3 e-mails mais recentes da conta Gmail autenticada.
    """
    try:
        access_token = authenticate_gmail()
        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', maxResults=3).execute()
        messages = results.get('messages', [])

        if not messages:
            return ResponseModel(success=True, response="📭 Nenhum e-mail encontrado na caixa de entrada.")

        email_data = []

        for msg in messages:
            msg_id = msg['id']
            message = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='metadata',
                metadataHeaders=['From', 'Subject']
            ).execute()

            headers = message.get('payload', {}).get('headers', [])
            subject = sender = 'Não encontrado'
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    sender = header['value']

            snippet = message.get('snippet', '')

            email_data.append(f"📧 *De:* {sender}\n📝 *Assunto:* {subject}\n🔍 *Resumo:* {snippet}\n------")

        response_message = "\n".join(email_data)

        return ResponseModel(
            success=True,
            response=response_message
        )

    except Exception as e:
        return ResponseModel(
            success=False,
            response=f"Ocorreu um erro ao listar os e-mails: {str(e)}"
        )