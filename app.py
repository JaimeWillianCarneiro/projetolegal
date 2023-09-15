from flask import Flask, render_template, request, redirect, make_response,  request, session
from flask_session import Session
from cryptography.fernet import Fernet
# import request
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


chave_secreta = Fernet.generate_key()


usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}
sessoes_ativas = {

}

# def criptografar_chave(chave: str):
def encrypt_string(input_string, key):
    # Gere um objeto de chave Fernet usando a chave fornecida
    cipher_suite = Fernet(key)

    # Converta a string de entrada em bytes
    input_bytes = input_string.encode('utf-8')

    # Criptografe a string
    encrypted_string = cipher_suite.encrypt(input_bytes)

    # Converta a saída criptografada em uma representação de string hexadecimal
    encrypted_hex_string = encrypted_string.hex()

    return encrypted_hex_string


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
        response.set_cookie("username", usuario)
        return response
    
    return render_template('login.html')


@app.route("/welcome")
def home():
    # return render_template("home.html")
    usuario = request.cookies.get("username")


    if usuario:
         return render_template("home.html", usuario= usuario)
    # if usuario in sessoes_ativas:
    #     usuario_info = sessoes_ativas[usuario]
    #     return render_template("home.html", usuario_info= usuario_info)
        
    else:
        return redirect('/login')


if __name__== "__main__":
    app.run(debug=True)
