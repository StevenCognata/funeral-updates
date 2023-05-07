from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for
from twilio.rest import Client

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'


# Twilio account SID and auth token
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# Store the phone numbers of users who have signed up
users = {}


# The message to send to users
message = 'Hello, world!'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's phone number from the form
        user_phone_number = request.form['phone']

        # Save the user's phone number and the current time
        users[user_phone_number] = datetime.now()

        # Send a text message to the user
        client.messages.create(
            body=message,
            from_='',
            to=user_phone_number
        )

        # Redirect the user to the confirmation page
        return render_template('confirmation.html')

    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global message

    # Check if the user is authenticated
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the information about the funeral
        name = request.form['name']
        church = request.form['church']
        cemetery = request.form['cemetery']

        # Create a new message with the funeral information
        message = f"Funeral for {name} at {church}. Burial at {cemetery}."

        # Clear the list of users who have signed up
        users.clear()

        # Redirect the admin to the confirmation page
        return render_template('admin_confirmation.html')

    return render_template('admin.html')

def clear_users():
    global users

    # Remove users who signed up more than 12 hours ago
    cutoff = datetime.now() - timedelta(hours=12)
    users = {k:v for k,v in users.items() if v > cutoff}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        if username == 'admin' and password == 'password':
            # If they are, set the 'admin' key in the session object
            session['admin'] = True

            # Redirect the user to the admin page
            return redirect(url_for('admin'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
