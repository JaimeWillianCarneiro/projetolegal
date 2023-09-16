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




json_file = 'sessions.json'
sessoes_ativas = {}
try:
    with open(json_file, 'r') as file:
         sessoes_ativas= json.load(file)
except FileNotFoundError:
    pass

usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}


"""
Essa biblioteca tive que achar na internet msm, 
queria ter usado alguma api tipo o site que vc 
mostrou na aula
Essa api ela gera uma entradad diferente toda vez que colocamos uma entrada, 
ou seja, se um usuario entrar diferentes vezes, gera diferentes tokens
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


def update_sessions_json():
    # Atualize o arquivo JSON com as sessões ativas
    with open(json_file, 'w') as file:
        json.dump(sessoes_ativas, file)

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
        chave = criptografar_chave(usuario,app.secret_key)
        if chave not in sessoes_ativas.keys():

            sessoes_ativas[chave] = {"user_name": usuario}
        else:
            del sessoes_ativas[chave]
            sessoes_ativas[chave] = {"user_name": usuario}

        response.set_cookie("user", chave)
        update_sessions_json()


        return response
    
    return render_template('login.html')


@app.route("/welcome")
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
@app.route('/active_sessions')
def get_active_sessions():
    # Retorne as sessões ativas como JSON
    return jsonify(sessoes_ativas)

if __name__== "__main__":
    app.run(debug=True)
