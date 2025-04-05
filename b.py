import smtplib
from email.message import EmailMessage
# Optionally import filetype for image type detection
# import filetype

PASSWORD = "bzjr gbma teff eqsm"  # Replace with your actual password
SENDER = 'joshanu55@gmail.com'
RECIEVER = 'joshanu55@gmail.com'

def send_email(image_path):
    email_message = EmailMessage()

    email_message['Subject'] = 'New customer showed up!'

    email_message.set_content('Hey, we just saw a new customer!')

    # Read the image file path
    with open(image_path, 'rb') as file:
        content = file.read()

    # Optionally use filetype to determine image type (if needed)
    # kind = filetype.guess(content)
    # if kind:
    #     maintype = 'image'
    #     subtype = kind.mime_type.split('/')[1]  # Extract subtype from MIME type
    # else:
    #     print("Could not determine image type")
    #     return

    # Set attachment details (assuming image)
    email_message.add_attachment(content, maintype='image', subtype='png')  # Replace with actual subtype if using filetype

    # Send out the Email (using port 465 for secure connection)
    gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Use port 465 for secure connection

    # SMTP communication routines (no need for starttls with port 465)
    gmail.ehlo()

    # Login with your credentials
    gmail.login(SENDER, PASSWORD)

    # Send the email
    gmail.sendmail(SENDER, RECIEVER, email_message.as_string())

    gmail.quit()


if __name__ == '__main__':
    send_email(image_path='images/20.png')
