from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import base64
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Setup Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def gmail_authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service):
    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="label:must-read", maxResults=3).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new emails found.")
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            try:
                payload = msg['payload']
                headers = payload.get("headers")
                subject = [i['value'] for i in headers if i["name"]=="Subject"][0]
                parts = payload.get("parts")[0]
                data = parts['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                summary = generate_summary(body)
                print(f"Subject: {subject}\nSummary: {summary}\n")
            except Exception as e:
                print(f"Failed to process email: {str(e)}")

def generate_summary(email_body):
    try:

        #summary = response.choices[0].text.strip()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"In 15 words, Summarize this email: {email_body}",
                },
            ],
        )
        summary = response.choices[0].message.content

        return summary
    except Exception as e:
        return f"Failed to generate summary: {str(e)}"

def main():
    service = gmail_authenticate()
    fetch_emails(service)

if __name__ == "__main__":
    main()
