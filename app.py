from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import Mail, Message
import random 

app = Flask(__name__)
app.secret_key = 'test'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jbcnrajveer@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rajveer@2009'

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def enter_email():
    if request.method == 'POST':
        email = request.form['email']
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['email'] = email
        
        try:
            msg = Message('Your OTP', sender='jbcnrajveer@gmail.com', recipients=[email])
            msg.body = f'Your OTP is {otp}'
            mail.send(msg)
            flash('OTP sent to your email!', 'success')
            return redirect(url_for('verifyotp'))
        except Exception as e:
            flash('Failed to send email. Please try again.', 'danger')
            print(e)
            
            return render_template('enter_email.html')
        
@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if int(entered_otp) == session.get('otp'):
            flash('Email verified successfully!', 'success')
            return redirect(url_for('enter_email'))
        else:
            flash('Invalid OTP. Please try again later.', 'danger')
            return redirect(url_for('verifyotp'))
        
        return render_template('verifyotp.html')
    
if __name__ == '__main__':
    app.run(debug=True)