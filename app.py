from flask import Flask, render_template, session
from flask.ext.cas import CAS,login_required
import config
import pickledb

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY

cas = CAS(app)

app.config['CAS_SERVER'] = config.CAS_SERVER
app.config['CAS_LOGIN_ROUTE'] = config.CAS_LOGIN_ROUTE
app.config['CAS_LOGOUT_ROUTE'] = config.CAS_LOGOUT_ROUTE
app.config['CAS_VALIDATE_ROUTE'] = config.CAS_VALIDATE_ROUTE
app.config['CAS_AFTER_LOGIN'] = config.CAS_AFTER_LOGIN

db = pickledb.load(config.DB_FILE, False)

@app.route("/")
@login_required
def main():
    return render_template('index.html',
        username = _get_username_clean(),
	is_coming = db.get(cas.username),
        count = len(db.getall())
    )

@app.route('/+1')
@login_required
def coming():
    db.set(cas.username, True)
    db.dump()  
    return render_template('index.html',
        username = _get_username_clean(),
	is_coming = db.get(cas.username),
        count = len(db.getall())
    )

@app.route('/-1')
@login_required
def notcoming():
    if db.get(cas.username):
        db.rem(cas.username)
        db.dump()  
    return render_template('index.html',
        username = _get_username_clean(),
	is_coming = db.get(cas.username),
        count = len(db.getall())
    )

def _get_username_clean():
    username = cas.username
    if(username == 'annesophie'){
    	first_name = 'Anne Sophie'
    }
    else {
    first_name = username.split('.')[0]
    first_name = first_name[0].upper() + first_name[1:]
    }
    if len(username.split('.')) > 1:
        last_name = username.split('.')[1]
        last_name = last_name[0].upper() + last_name[1:]
        return first_name + ' ' +last_name
    else:
        return first_name



if __name__ == "__main__":
    app.run()
