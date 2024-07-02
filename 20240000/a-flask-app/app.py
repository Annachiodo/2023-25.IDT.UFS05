from flask import Flask, redirect, render_template, request
import os

appWeb = Flask(__name__)

#http://www.miosito.it/prova
#http://www.miosito.it/saluto

#http://www.miosito.it/

class Utente:
    def __init__(self, nome, cognome, username, password, email, data_di_nascita, genere):
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.email = email
        self.data_di_nascita = data_di_nascita
        self.genere = genere

    def ottieni_nome(self):
        return self.nome
    
    def ottieni_cognome(self):
        return self.cognome

    def ottieni_username(self):
        return self.username
    
    def ottieni_password(self):
        return self.password

    def ottieni_email(self):
        return self.email

    def ottieni_data_di_nascita(self):
        return self.data_di_nascita

    def ottieni_genere(self):
        return self.genere
    


Utente1 = Utente("Mario", "Rossi", "mrossi", "1234567", "mario.rossi@gmail.com", "01/01/1980", "Maschio")
Utente2 = Utente("Giovanni", "Bianchi", "gbianchi", "qwerty", "giovanni.bianchi@gmail.com", "15/05/1990", "Maschio")
Utente3 = Utente("Roberta", "Verdi", "rverdi", "ciao1", "roberta.verdi@gmail.com", "10/10/1985", "Femmina")
lista_utenti = [
    Utente1, Utente2, Utente3
]

global loggedUser
loggedUser = None



@appWeb.route("/")
def main():
    return "pagina iniziale da visualizzare"

@appWeb.route("/prova")
def prova():
    return "stringa da visualizzare come prova"
@appWeb.route("/presentazione")
def saluto():
    return "Buongiorno"

@appWeb.route("/index")
def index():
    return render_template("index.html")

@appWeb.route("/htmlsample")
def html():
    return "<html><body><h1>Titolo</h1><p>paragrafo da visualizzare</p></body></html>"

@appWeb.route("/login")
def login():
    return render_template("login.html")

@appWeb.route("/registrazione")
def registrazione():
    return render_template("registrazione.html")

@appWeb.route("/home")
def home():
    return render_template("home.html", paramUser = loggedUser)


@appWeb.route("/autenticazione", methods = ["POST"])
def autenticazione():
    usernameStr = request.form.get("username")
    passwordStr = request.form.get("password")
    for utente in lista_utenti:
        if usernameStr == utente.ottieni_username() and passwordStr == utente.ottieni_password():
            loggedUser = utente
            return render_template("home.html", paramUser=loggedUser)
    return render_template("fail.html")

@appWeb.route("/registrazione_post", methods = ["POST"])
def registrazione_post():
    nameStr = request.form.get("name")
    cognomeStr = request.form.get("cognome")
    usernameStr = request.form.get("username")
    passwordStr = request.form.get("password")
    emailStr = request.form.get("email")
    datadinascitaStr = request.form.get("data di nascita")
    genereStr = request.form.get("genere")
    utente = Utente(nameStr,cognomeStr,usernameStr,passwordStr,emailStr,datadinascitaStr,genereStr)
    global loggedUser
    loggedUser = utente
    lista_utenti.append(utente)

    return redirect("/home")

if __name__ == "__main__":
    # https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings
    # SERVER_PORT Read-only. The port the app should listen to.
    if "PORT" in os.environ:
        appWeb.run(host="0.0.0.0", port=os.environ['PORT'])
    else:
        appWeb.run(host="0.0.0.0")



Conversazioni
Spazio utilizzato: 0,16 GB
Norme del programma
Powered by Google
Ultima attività dell'account: 4 ore fa
Dettagli
from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import os
import requests

class User:
    username = None
    password = None
    email = None

    def __init__(self, u, p, e):
        self.username = u
        self.password = p
        self.email = e
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    '''def __str__(self):
        return f"User: {self.username}, {self.password}, {self.email}"
    '''
    def __repr__(self):
        return f"Lista utenti: username {self.username}, password {self.password}, e-mail {self.email}"
    

antonio = User("antonio", "123456", "antonio@itsrizzoli.it")
davide = User("davide", "ciao", "d.longo@itsrizzoli.it")
aimane = User('aimane', 'yolo', 'a.jrada@itsrizzoli.it')
kristian = User('kristian', 'ciaone', 'k.salva@itsrizzoli.it')
listaUser = [antonio, davide, aimane, kristian]



appWeb = Flask(__name__)
def initialize_database():
    try:
        # Connessione senza specificare il database, per permettere la creazione del database stesso
        connection = mysql.connector.connect(
            host="its-rizzoli-idt-mysql-33593.mysql.database.azure.com",
            user="psqladmin",
            passwd="H@Sh1CoR3!"
        )
        cursor = connection.cursor()

        # Leggere il contenuto del file SQL
        with open('script.sql', 'r') as file:
            sql_commands = file.read().split(';')

        # Eseguire ogni comando SQL
        for command in sql_commands:
            if command.strip():  # Ignora comandi vuoti
                cursor.execute(command)

        # Commit delle modifiche
        connection.commit()

        cursor.close()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")

@appWeb.route("/")
def main():
    connection = None
    risposta = "nessuna risposta"
    try:
        connection = mysql.connector.connect(
            host="its-rizzoli-idt-mysql-33593.mysql.database.azure.com",
            user="psqladmin",
            passwd="H@Sh1CoR3!",
            database="ufs05db"
        )
        risposta = "Connection to MySQL DB successful"
        cursor = connection.cursor()

        query = ("SELECT first_name, last_name FROM employees")
        cursor.execute(query)

        for (first_name, last_name) in cursor:
            risposta = first_name +last_name
        cursor.close()
        connection.close()
    except Error as e:
        risposta = f"The error '{e}' occurred"
    return  risposta

@appWeb.route("/registrazione")
def registrazione():
    return render_template("registrazione.html")


@appWeb.route("/autenticazione", methods = ["POST"])
def autenticazione():
    usernameStr = request.form.get("username")
    passwordStr = request.form.get("password")
    for i in listaUser:
        u = i.getUsername()
        p = i.getPassword()
        if u == usernameStr and p == passwordStr:
            return render_template("home.html", paramUser = usernameStr)
                
    return render_template("fail.html") # messo fuori perché altrimenti non finisce il ciclo for, e si ferma alla prima iterazione
            
    '''if passwordStr == "123456":
        return render_template("home.html", paramUser = usernameStr)
    else:
        return render_template("fail.html")'''

    '''for i in listaUser:
        listaUser.append(usernameStr)
        return render_template("listaUser.html", paramUser = listaUser)'''

@appWeb.route("/saveuser", methods =["POST"])
def saveuser():
    usernameStr = request.form.get("username")
    passwordStr = request.form.get("password")
    emailStr = request.form.get("email")
    listaUser.append(User(usernameStr, passwordStr, emailStr))


    url ="https://nodered-32761.azurewebsites.net/ciaone?usernameStr={}&emailStr={}".format(usernameStr, emailStr)


# data = {'nome': 'anna', 'cognome': 'chiodo'}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(url)

#2) aggiungere il body alla req

#html = response.read()

    return render_template("listaUtenti.html", paramList = listaUser)

if __name__ == "__main__":
        # Inizializza il database
    initialize_database()
    # https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings
    # SERVER_PORT Read-only. The port the app should listen to.
    if "PORT" in os.environ:
        appWeb.run(host="0.0.0.0", port=os.environ['PORT'])
    else:
        appWeb.run(host="0.0.0.0")