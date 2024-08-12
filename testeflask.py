#Importação de bibliotecas
import os  #Biblioteca de acesso a arquivos do sistema operacional.
from flask import Flask, render_template, request, url_for, redirect  #Biblioteca flask
from flask_sqlalchemy import SQLAlchemy  #Biblioteca ORM sqlalchemy para flask

basedir = os.path.abspath(os.path.dirname(__file__))  #Definição do caminho(path) raíz(root)
app = Flask(__name__)  #Definição de aplicação flask
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(basedir, 'database.db'))  # Definição do tipo de banco e nome do arquivo do banco.
db = SQLAlchemy(app)


#Models para o banco de dados

class Produto(db.Model): #Criação do model Produto como objeto.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    lucro = db.Column(db.Float, nullable=False)


class Trabalhador(db.Model): #Criação do model Trabalhador como objeto.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)


#Rotas Produtos
@app.route('/visualizar_produto', methods=['GET'])
def visualizar_produto():
    return render_template('index.html')


@app.route('/cadastrar_produto', methods=['GET'])
def cadastro_produto():
    return render_template('index.html')


@app.route('/deletar_produto/<int>', methods=['GET'])
def deletar_produto(int):
    return render_template('index.html')


#Rotas Trabalhador
@app.route('/visualizar_trabalhador', methods=['GET'])
def visualizar_trabalhador():
    return render_template('index.html')


@app.route('/cadastrar_trabalhador', methods=['GET'])
def cadastrar_trabalhador():
    return render_template('index.html')


@app.route('/deletar_trabalhador/<int>', methods=['GET'])
def deletar_trabalhador(int):
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
