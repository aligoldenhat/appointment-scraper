from twilio.rest import Client
from pushover import Client as Cl
import os
from time import sleep

ali_phone = ""
ali_account_sid = ''
ali_auth_token = ''
ali_twilio = ''

def call_to_my_phone(phone_number, SID, Token, twilio_phonenumber):
    account_sid = SID
    auth_token = Token
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            twiml='<Response><Say>Ahoy, World!</Say></Response>',
                            to = phone_number,
                            from_= twilio_phonenumber
                        )


def push_notif(title, body, PRIORITY, captcha_img = None ):
    client = Cl("g5mb4is5rdznm9s9uuv7sxjgn6x1ht", api_token="af4yppzfpz7xa435z16czw9cccxoqt")
    if captcha_img == None:
        client.send_message(body, title=title, priority=PRIORITY, expire=1000, retry=30, sound = 'alien')
    else:
        dir = os.path.join(os.path.dirname(__file__), f'./Ss_captcha/{captcha_img}.png')
        with open(dir, 'rb') as image:
            client.send_message(body, title=title, priority=PRIORITY, expire=1000, retry=30, sound = 'alien', attachment=image)


