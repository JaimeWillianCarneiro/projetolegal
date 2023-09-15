from flask import Flask, render_template, request, redirect, make_response, session

# import request
app = Flask(__name__)




usuarios= {
    "Jaime": "senha", 
    "Willian": "123456", 
    "Hendryk": "Coxinha"
}
sessoes_ativas = {

}
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
        
        #return render_template("home.html" , user = usuario)
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
    else:
        return redirect('/login')


if __name__== "__main__":
    app.run(debug=False)
