from flask import Flask, render_template, request, redirect, make_response,  request, session,jsonify
from flask_session import Session
from cryptography.fernet import Fernet 
import json
# import request
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = Fernet.generate_key()
Session(app)





usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}
sessoes_ativas = {}

"""
Essa biblioteca tive que achar na internet msm, 
queria ter usado alguma api tipo o site que vc 
mostrou na aula
"""
def criptografar_chave(entrada, chave_secreta):
    # Gera um objeto de chave Fernet usando a chave fornecida
    chave_objeto = Fernet(chave_secreta)

    # Converta a string de entrada em bytes
    bytes = entrada.encode('utf-8')

    # Criptografe a string
    entrada_criptografada = chave_objeto.encrypt(bytes)

    # Converta a saída criptografada em uma representação de string hexadecimal
    cripto_hexa= entrada_criptografada.hex()

    return cripto_hexa


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
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
        sessoes_ativas[criptografar_chave(usuario,app.secret_key)] = {"user_name": usuario}
        response.set_cookie("user",criptografar_chave(usuario,app.secret_key))
        


        return response
    
    return render_template('login.html')


@app.route("/welcome")
def home():
    # return render_template("home.html")
    usuario = request.cookies.get("user")


    if usuario:
         nome = sessoes_ativas[usuario]
         return render_template("home.html", usuario= usuario, nome = nome)
    # if usuario in sessoes_ativas:
    #     usuario_info = sessoes_ativas[usuario]
    #     return render_template("home.html", usuario_info= usuario_info)
        
    else:
        return redirect('/login')


if __name__== "__main__":
    app.run(debug=True)
