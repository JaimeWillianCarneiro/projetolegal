from flask import Flask, render_template, request
# import request
app = Flask(__name__)



@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')


usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # if usuario is None:
        #     return render_template("login", mensagem = "Inserir usuário é brigatório;")
        if usuario not in usuarios.keys():
            return render_template("login.html", mensagem= "O usuário e/ou senha incorreto  usuaro")

        user_password = usuarios[usuario]
        if senha!= user_password:
            return render_template("login.html", mensagem= "O usuário e/ou senha incorreto")
        
        return render_template("home.html" , user = usuario)

        

    return render_template('login.html')



if __name__== "__main__":
    app.run(debug=True)

