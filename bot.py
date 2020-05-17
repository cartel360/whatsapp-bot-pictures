from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from storage import dropbox_folder_from, save_on_dropbox


app = Flask(__name__)


@app.route('/reply', methods=['POST'])
def reply():
    num_media = int(request.values['NumMedia'])
    media = request.values.get('MediaContentType0', '')
    user_phone_number = request.values['From']

    if user_phone_number.startswith('whatsapp'):
        # from format: 'whatsapp:+490001112223'
        user_phone_number = user_phone_number.split(':')[1]

    resp = MessagingResponse()
    reply = f"I didn't get it 😕"  # default message

    if num_media > 0:
        if media.startswith('image/'):
            file_url = request.values['MediaUrl0']
            extension = media.split('/')[1]
            save_on_dropbox(user_phone_number, file_url, extension)
            reply = 'Your pic is safe and sound!'
        else:
            reply = 'Sorry, only pictures are allowed.'
    else:
        user_message = request.values['Body'].lower()
        if 'save' in user_message:
            reply = (
                f"Let's get started! From now on, I'll save the pics you send to me.\n"
                "To see your pics, just send me a message with the word *see*."
            )
        elif 'see' in user_message:
            all_pics_url = dropbox_folder_from(user_phone_number)
            reply = f'Here you go: {all_pics_url}'
    resp.message(reply)
    return str(resp)
