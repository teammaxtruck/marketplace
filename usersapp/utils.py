from django.core.mail import EmailMessage

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
     # from_email='os.environ.get('EMAIL_FROM')',
   #   from_email='ayman.mohammad@gmail.com',
      from_email='moham_aym@yahoo.com',
      to=[data['to_email']]
    )
    email.send()