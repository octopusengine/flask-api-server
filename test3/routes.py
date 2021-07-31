from flask import render_template, request, redirect, url_for, session, send_file
from flask import current_app as app
from flask_qrcode import QRcode
import random, json, httpx
from .agama3 import add_log, log_tail, bitcoin_usd, print_octopus, system_info
from .agama3db import db_log_list, add_msg_txt, tail_msg_txt, tail_msg_list
from .agama3extern import my_auth
# import requests

qrcode = QRcode(app)

main_msg="..."  #ag()
AUTH3 = my_auth()

@app.route('/')
def index():
    ll = db_log_list()
    add_log("/   ")
    return render_template('index.html', msg=main_msg,last=ll[0])


@app.route('/test')
def test():
    add_log("test")
    var_num = bitcoin_usd()
    #var_num = random.randint(10000,99999)
    return render_template('test.html', varnum=str(var_num))


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    add_log("auth")
    if request.method == "POST":
       key = request.form.get("key")
       if key == AUTH3:
          return render_template('info.html', sys_info = system_info())
    return render_template('auth.html')


@app.route('/links')
def links():
    add_log("link")
    return render_template('links.html', msg=main_msg)


@app.route('/page2')
def page2():
    return render_template('page2.html', msg=main_msg)


@app.route('/info3')
def info3():
   add_log("info")
   ibase = "(you.tor.nginx.uwsgi.flask.me)\n"
   ret_str="<br /><hr /><pre>"
   ret_str += print_octopus()
   ret_str += ibase
   ret_str += system_info()
   ret_str += "| info3 | page2 | success | form_in | <br /><br />"
   ret_str += tail_msg_txt() + "<hr />"
   ll = db_log_list()
   #ret_str += str(ll)
   for li in ll:
      ret_str += str(li) + "<br />" 
   ret_str += "</pre><hr />"
   return ret_str


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/form_in', methods=['POST', 'GET'])
def form_in():

    if request.method == "POST":
       key = request.form.get("key")
       if key == AUTH3:
           return "ok, you are welcome"
       return "key is {}.".format(key)


    return '''<br /><hr /><form method="POST">
    key <input type="text" name="key">
    <input type="submit">
    </form><hr />'''


@app.route('/led1', methods=['POST', 'GET'])
def led1():

    rc = ""
    if request.method == "POST":
       key = request.form.get("act")
       rc = "key is {}.".format(key)
       if key == "on":
           action="https://octopuslab.cz/api/led1.php?light=on"
           try:
             res = httpx.get(action)
             rc = "ok, on (" + str(res) + ")"
           except:
             rc = "server.err"
       if key == "off":
           action="https://octopuslab.cz/api/led1.php?light=off"
           try:
             res = httpx.get(action)
             rc = "ok, off (" + str(res) + ")"
           except:
             rc = "server.err"


    rc += '''<br /><hr /><form method="POST">
    action <input type="text" name="act">
    <input type="submit">
    </form><hr />'''
    return rc


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    add_log("chat")

    if "nick" in session:
       form_nick = session["nick"]
    else:
       form_nick = "anonymous"

    if request.method == "POST":
       nick = request.form.get("nick")
       msg = request.form.get("msg")

       if (len(msg) > 1) and (nick != "anonymous"):
          session["nick"] = nick
          add_msg_txt(nick,msg)

    msg_list = tail_msg_list(12)
    return render_template('chat.html', form_nick = form_nick, msg_list=msg_list)


@app.route("/qrcode", methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")


#from flask import Flask, redirect, url_for, request
#app = Flask(__name__)

