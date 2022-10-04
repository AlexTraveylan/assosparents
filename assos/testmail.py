# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# SENDGRID_API_KEY=''

# message = Mail(
#     from_email='ne-pas-repondre@parent-nelson-mandela.xyz',
#     to_emails='timothee.demares@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     # sg = SendGridAPIClient()
#     # response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e)