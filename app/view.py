# app/views.py
from flask import render_template, request, redirect, url_for, flash, Blueprint
import json

from . import app

view =  Blueprint('auth', __name__)

# Função para ler as notas do arquivo JSON
def ler_notas():
    try:
        with open('notas.json', 'r') as file:
            notas = json.load(file)
    except FileNotFoundError:
        notas = []
    return notas


json_file = 'sessions.json'

try:
    with open(json_file, 'r') as file:
         sessoes_ativas= json.load(file)
except FileNotFoundError:
    pass

# Rota para exibir todas as notas
# @view.route('/')
# def index():
#     notas = ler_notas()
#     return render_template('index.html', notas=notas)


@view.route('/')
@view.route('/criar_nota', methods=['GET', 'POST'])
def criar_nota():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        # criador = session.get('usuario_id')  # Supondo que você tenha informações de usuário em sessões
        criador = request.cookies.get("user")
        notas = ler_notas()
        notas.append({'titulo': titulo, 'conteudo': conteudo, 'criador': criador})
        with open('notas.json', 'w') as file:
            json.dump(notas, file)
        flash('Nota criada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('home.html')

# Rota para editar uma nota existente
@view.route('/editar_nota/<int:id>', methods=['GET', 'POST'])
def editar_nota(id):
    notas = ler_notas()
    nota = notas[id]
    if request.method == 'POST':
        nota['titulo'] = request.form['titulo']
        nota['conteudo'] = request.form['conteudo']
        with open('notas.json', 'w') as file:
            json.dump(notas, file)
        flash('Nota editada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('nota_form.html', nota=nota)

# Rota para excluir uma nota
@view.route('/excluir_nota/<int:id>')
def excluir_nota(id):
    notas = ler_notas()
    if id < len(notas):
        del notas[id]
        with open('notas.json', 'w') as file:
            json.dump(notas, file)
        flash('Nota excluída com sucesso!', 'success')
    return redirect(url_for('index'))

@view.route('/notas')
def exibir_notas():
    notas = ler_notas()
    # Filtrar as notas do usuário atual (você deve adaptar essa lógica)
    # usuario_atual = session.get('usuario_id')  # Suponha que você tenha o ID do usuário na sessão
    
    usuario_atual =   request.cookies.get("user")
    notas_do_usuario = [nota for nota in notas if nota.get('criador') == usuario_atual]
    return render_template('minhasnotas.html', notas=notas_do_usuario)