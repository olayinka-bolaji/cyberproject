from email import message
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings

class SendMail:
    def __init__(self, to, subject, message, altmsg):
        self.to = to
        self.subject = subject
        self.message = message
        self.altmsg = altmsg
        self.send()
        print("Email sent successfully")

    def send(self):
        port = settings.MAIL_PORT # For starttls
        smtp_server = settings.MAIL_SERVER
        sender_email = settings.MAIL_USER
        password = settings.MAIL_PASS
        receiver_email = self.to

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = self.altmsg
        html = self.message

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())


class EmailMessages:
    def __init__(self, token, username):
        self.token = token
        self.url = settings.PROD
        self.username = username
    def registerMsg(self):
        msg = f'''<div style="background: #eee;padding: 10px;">
                                <div style="max-width: 500px;margin: 0px auto;font-family: sans-serif;text-align: center;background: #fff;border-radius: 5px;overflow: hidden;">
                                    <div style="width: 100%;background: #fc9700;">
                                        <h1 style="color: #fff;text-decoration: none;margin: 0px;padding: 10px 0px;">Cyber Arena</h1>
                                    </div>
                                    <div style="color: #000;padding: 10px;margin-top: 10px;">
                                        Hello {self.username}, <br/>Thank you for registering with us at Cyber Arena. Please login to your dashboard with your email and password
                                        <div style="padding: 10px;margin: 10px 0px;color: #000;background: #eee;border-radius: 5px; height: 80px;">
                                        Account Confirmation:
                                            <p><a style="margin:10px; padding: 10px; width: 100px; height: 45px; background-color: #fc9700; font-size: 35px; color: #fff;font-weight: 700; border-radius: 5px; text-decoration: none;" href="{self.url}confirm/{self.token}">
                                                Confirm
                                            </a></p>
                                        </div>
                                    </div>
                                    <div style="color: #000; padding-bottom: 10px;">
                                        However, if this registration process was not initiated by you, kindly ignore this mail.
                                        <br />
                                        If you have encounter any problem while creating your account, feel free to <a href="{self.url}contact" style="text-decoration: none; color: #bf5794;">contact us</a>
                                    </div>
                                </div>
                            </div>'''

        alt = f'''Hello user, Thank you for registering with us at Cyber Arena. Please login to your dashboard with your email and dashboard. <br />  However, if this registration process was not initiated by you, kindly ignore this mail.'''

        return msg, alt

    def resetPasswordMsg(self, email):
        msg = f'''<div style="background: #eee;padding: 10px;">
                                <div style="max-width: 500px;margin: 0px auto;font-family: sans-serif;text-align: center;background: #fff;border-radius: 5px;overflow: hidden;">
                                    <div style="width: 100%;background: #fc9700;">
                                        <h1 style="color: #fff;text-decoration: none;margin: 0px;padding: 10px 0px;">Cyber Arena</h1>
                                    </div>
                                    <div style="color: #000;padding: 10px;margin-top: 10px;">
                                        Hello,
                                        we've received a request to reset the password for the Cyber Arena account associated with {email}. No changes have been made to your account yet.
                                        You can reset your password by clicking the link below:
                                        <div style="padding: 10px;margin: 10px 0px;color: #000;background: #eee;border-radius: 5px; height: 80px;">
                                            <p><a style="margin:10px; padding: 10px; width: 100px; height: 45px; background-color: #fc9700; font-size: 35px; color: #fff;font-weight: 700; border-radius: 5px; text-decoration: none;" href="{self.url}reset/{self.token}">
                                                Reset password
                                            </a></p>
                                        </div>
                                    </div>
                                    <div style="color: #000; padding-bottom: 10px;">
                                        If you did not request a new password please let us know immediately by contacting us.
                                       <a href="{self.url}contact" style="text-decoration: none; color: #bf5794;">contact us</a>
                                    </div>
                                </div>
                            </div>'''
        alt = ""

        return msg, alt

    def passChangedMsg(self):
        msg = f'''<div style="background: #eee;padding: 10px;">
                                <div style="max-width: 500px;margin: 0px auto;font-family: sans-serif;text-align: center;background: #fff;border-radius: 5px;overflow: hidden;">
                                    <div style="width: 100%;background: #fc9700;">
                                        <h1 style="color: #fff;text-decoration: none;margin: 0px;padding: 10px 0px;">Cyber Arena</h1>
                                    </div>
                                    <div style="color: #000;padding: 10px;margin-top: 10px;">
                                        Password reset was successful
                                        <div style="padding: 10px;margin: 10px 0px;color: #fff;background: #fc9700;border-radius: 5px; height: 80px;">
                                            <p>Awesome! you have successfully updated your password</p>
                                        </div>
                                    </div>
                                    <div style="color: #000; padding-bottom: 10px;">
                                        If you did not request a new password please let us know immediately by contacting us.
                                       <a href="{self.url}contact" style="text-decoration: none; color: #bf5794;">contact us</a>
                                    </div>
                                </div>
                            </div>'''
        alt = ""

        return msg, alt
