import smtplib
from email.message import EmailMessage
import imghdr

PASSWORD = "bzjr gbma teff eqsm"
SENDER = 'joshanu55@gmail.com'
RECIEVER = 'joshanu55@gmail.com'
PORT = 465

def send_email(image_path):
    print("Email function started")
    email_message = EmailMessage()

    # This object behaves like a dictionary, We have to provide the email subject, and  the values for the 'subject' key 
    email_message['Subject'] = 'New customer showed up!'
    
    # Body of the Email
    email_message.set_content('Hey, we just saw a new customer!')
    
    # Read the image file path
    with open(image_path , 'rb') as file:
        content = file.read()
    
    # Add attachment, specify the maintype of file and supply a subtype argument, if it is a .png on .jpg
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))  

    # Send out the Email
    gmail = smtplib.SMTP_SSL('smtp.gmail.com', PORT) # Note: the port for gmail is '587' or '465'

    # Routines to start the eamil server parameter
    gmail.ehlo()
    #gmail.starttls()

    # Point to gmail, which is the SMTP instance
    gmail.login(SENDER, PASSWORD)

    # Sending Email as a string
    gmail.sendmail(SENDER, RECIEVER, email_message.as_string())
    
    # Quit SMTP server object
    gmail.quit()
    print("Email function Ended")


if __name__ == '__main__':
    send_email(image_path='images/20.png')


