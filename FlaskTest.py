from flask import Flask, render_template, abort, redirect, request, url_for, make_response, session
from DbClass import Dbclass
from flask.ext.session import Session
import RPi.GPIO as GPIO
from Game import BattleShipGame

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Open SPI bus
GPIO.setmode(GPIO.BCM)

@app.route('/')
@app.route('/index/')
def index():
    db = Dbclass()
    UserID = session.get('UserID', 'notset')

    if UserID == "notset":
        return render_template('index.html')
    else:
        User = db.GetUserByID(UserID)
        return render_template('index.html', user=User)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/tutorial')
def tutorial():
    return render_template('Tutorial.html')


@app.route('/login', methods=["GET",'POST'])
def login():
    error = None
    db = Dbclass()

    UserID = session.get('UserID', 'notset')

    if UserID == "notset":
        if request.method == 'POST':
            if request.form["bsubmit"] == "Login":
                username = request.form['username']
                Password = request.form['password']

                User = db.GetUserByName(username)

                print(User)

                if username == User[1] and Password == User[2]:
                    #return render_template('index.html', user=username)
                    session['UserID'] = User[0]

                    return redirect(url_for('index', userID=User[0]))
                else:
                    error = 'Invalid Credentials. Please try again.'
            elif request.form["bsubmit"] == "Register":
                return redirect(url_for('register'))
        return render_template('login.html', error=error)
    else:
        return redirect(url_for('index', userID=session.get('UserID', 'notset')))


@app.route('/register', methods=["GET",'POST'])
def register():
    error = None
    db = Dbclass()

    if request.method == 'POST':
        if request.form["bsubmit"] == "Register":
            Username = request.form['username']
            Password = request.form['password']
            Password2 = request.form['passwordSecond']
            email = request.form['email']

            if Password == Password2:
                # Query om user toe te voegen oproepen.
                db.InsertUser(Username, Password, email)
                return redirect(url_for('login'))
            else:
                error = "Passwords don't match"

    return render_template('register.html', error=error)


@app.route('/PlayGame', methods=["GET",'POST'])
def playGame():
    UserID = session.get('UserID', 'notset')

    if UserID == "notset":
        error = "not logged in!"
        return render_template('PlayGame.html', error=error)
    else:
        db = Dbclass()
        User = db.GetUserByID(UserID)
        if request.method == 'POST':
            if request.form["bsubmit"] == "Play":
                Game = BattleShipGame()

                score = Game.StartGame()

                if score == 1:
                    db = Dbclass()
                    User = db.GetUserByID(UserID)
                    db.Connect()
                    db.SetWinInHistoryOnPlayerID(User[0], 0)
                    return render_template('PlayGame.html', user=User, score="won")
                else:
                    return render_template('PlayGame.html', user=User, score="lost")
        else:
            return render_template('PlayGame.html', user=User)


@app.route('/profile', methods=["GET",'POST'])
def profile():
    error = None
    db = Dbclass()

    UserID = session.get('UserID', 'notset')


    if UserID == "notset":
        error = "Please login first to begin playing!"
        return render_template('profile.html', error=error)
    else:
        User = db.GetUserByID(UserID)
        db.Connect()
        Won = db.GetUserWonHistory(UserID)
        db.Connect()
        Lost = db.GetUserLostHistory(UserID)

        error = ""
        return render_template('profile.html', error=error, user=User, won=Won, lost=Lost)

if __name__ == '__main__':
    # debugger aanzetten MAAR vanaf de website online staat (productie) zet je deze terug uit
    app.run(debug=True, host='0.0.0.0')

