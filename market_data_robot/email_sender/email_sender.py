import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd


class SslGmailSender:
    """
    Based on the examples presented on: https://realpython.com/python-send-email/
    """

    def __init__(self, str_sender_email: str, str_password, int_port: int = 465):
        self.int_port = int_port
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = str_sender_email
        self.password = str_password

    def send_email_with_csv_and_fig_attachment(
            self, str_email_text: str, str_receiver: str, str_subject: str, df: pd.DataFrame, fig = None

    ):
        # -------------- prepare the email object --------------
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = str_receiver
        message["Subject"] = str_subject
        # attach the text
        message.attach(MIMEText(str_email_text, "plain"))
        # -------------- attach the dataframe as CSV --------------
        df.to_csv("temp.csv")
        file = open("temp.csv", "rb")
        message.attach(MIMEApplication(file.read(), Name="data_file.csv"))
        file.close()
        # -------------- attach the figure --------------
        if fig is not None:
            fig.savefig("temp.png")
            fig_file = open("temp.png", "rb")
            message.attach(MIMEImage(fig_file.read(), name="image_file.png"))
            fig_file.close()
        # -------------- send the email --------------
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self.smtp_server, self.int_port, context=context)
        server.login(user=self.sender_email, password=self.password)
        server.sendmail(self.sender_email, str_receiver, message.as_string())

    def send_text_only_message(self, str_text: str, str_receiver_email: str):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self.smtp_server, self.int_port, context=context)
        server.login(user=self.sender_email, password=self.password)
        server.sendmail(self.sender_email, str_receiver_email, str_text)


# sender = SslGmailSender(
#     str_sender_email="market.robot.mailbox@gmail.com",
#     str_eniron_var_pass="MARKET_DATA_ROBOT_GMAIL_PASSWORD"
# )
# sender.send_text_only_message(str_text="Test message!", str_receiver_email="awegrzyn17@gmail.com")


