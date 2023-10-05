from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, make_response,  request, session,jsonify
# from flask_session import Session

import hashlib
import json

auths = Blueprint('auths', __name__)

usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}


json_file = 'sessions.json'
sessoes_ativas = {}
try:
    with open(json_file, 'r') as file:
         sessoes_ativas= json.load(file)
except FileNotFoundError:
    pass




def update_sessions_json():
    # Atualize o arquivo JSON com as sessões ativas
    with open(json_file, 'w') as file:
        json.dump(sessoes_ativas, file)



@auths.route("/", methods=["GET", "POST"])
@auths.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

       
        if usuario not in usuarios.keys():
            return render_template("login.html", mensagem= "O usuário e/ou senha incorreto")

        user_password = usuarios[usuario]
        if senha!= user_password:
            return render_template("login.html", mensagem= "O usuário e/ou senha incorreto")
        
        # return render_template("home.html" , user = usuario)
        response = make_response(redirect("/welcome"))
        # response.set_cookie("username", usuario)

        """
        Alteração:
        """

        # chave = criptografar_chave(usuario,app.secret_key)
        chave = hashlib.sha256(usuario.encode()).hexdigest()
        if chave not in sessoes_ativas.keys():

            sessoes_ativas[chave] = {"user_name": usuario}
        else:
            del sessoes_ativas[chave]
            sessoes_ativas[chave] = {"user_name": usuario}

        response.set_cookie("user", chave)
        update_sessions_json()


        return response
    
    return render_template('login.html')



@auths.route("/welcome")
def home():
    # return render_template("home.html")
    usuario = request.cookies.get("user")

    sessoes = sessoes_ativas.values()
    if usuario:
        nomes = sessoes_ativas[usuario]
        nome = nomes['user_name']
        return render_template("home.html", usuario= usuario, sessoes = sessoes, nome = nome)
    # if usuario in sessoes_ativas:
    #     usuario_info = sessoes_ativas[usuario]
    #     return render_template("home.html", usuario_info= usuario_info)
        
    else:
        return redirect('/login')