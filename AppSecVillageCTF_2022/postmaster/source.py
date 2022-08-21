from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import flask
import re
import smtplib

# This is just the regex browsers use for <input type="email">
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}'
    r'[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)

app = flask.Flask(__name__)
app.config.from_object('config')


@app.route('/send_email', methods=['POST'])
def send_email():
    name = flask.request.form['name']
    email_address = flask.request.form['email']

    if '\n' in name or '\r' in name:
        return flask.redirect('/?m=badname')
    if not EMAIL_REGEX.match(email_address):
        return flask.redirect('/?m=bademail')

    mail = MIMEMultipart('alternative')
    mail['From'] = 'postmaster.boats <noreply@postmaster.boats>'
    mail['To'] = name + ' <' + email_address + '>'
    if email_address == 'admin@email.invalid':
        mail['Subject'] = 'Flag'
        mail.attach(MIMEText(app.config['FLAG'], 'plain'))
    else:
        mail['Subject'] = 'Sorry, try again'
        mail.attach(MIMEText('No flag for you :(', 'plain'))

    smtp_client = smtplib.SMTP(timeout=2)
    smtp_client.connect('localhost')
    smtp_client.send_message(mail)

    return flask.redirect('/?m=sent')


@app.route('/source')
def source():
    with open(__file__) as this_file:
        return this_file.read(), {'Content-Type': 'text/plain'}


@app.route('/')
def home():
    return flask.render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)