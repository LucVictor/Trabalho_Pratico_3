#Importação de bibliotecas
import os  #Biblioteca de acesso a arquivos do sistema operacional.
from flask import Flask, render_template, request, url_for, redirect, flash  #Biblioteca flask
from flask_sqlalchemy import SQLAlchemy  #Biblioteca ORM sqlalchemy para flask

basedir = os.path.abspath(os.path.dirname(__file__))  #Definição do caminho(path) raíz(root)
app = Flask(__name__)  #Definição de aplicação flask
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(basedir, 'database.db'))  # Definição do tipo de banco e nome do arquivo do banco.
db = SQLAlchemy(app)

#Variáveis constantes globais de limite
LIMITE_DE_TRABALHADOR = 2  #Limite definido pelo modelo
LIMITE_DE_PRODUTOS = 3  #Limite defenido pelo modelo


#Models para o banco de dados

class Produto(db.Model):  #Criação do model Produto como objeto.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    rentabilidade = db.Column(db.Float, nullable=False)


class Trabalhador(db.Model):  #Criação do model Trabalhador como objeto.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    custo = db.Column(db.Float, nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)


#Rotas Produtos
@app.route('/visualizar_produtos', methods=['GET'])
def visualizar_produtos():
    produtos = Produto.query.all() #Variável recebe todos os produtos do banco de dados.
    return render_template('visualizar_produtos.html', produtos=produtos)


@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastro_produto():
    global LIMITE_DE_PRODUTOS #Importa a variável constante para dentro do escopo da função
    if int(Produto.query.count()) == LIMITE_DE_PRODUTOS: #Bloqueia o acesso caso o número de produtos seja igual ao limite.
        return redirect(url_for('visualizar_produtos'))
    if request.method == 'POST':
        try:
            produto = Produto(nome=request.form['nome'], rentabilidade=request.form['rentabilidade'])
            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('visualizar_produtos'))
        except:
            return redirect(url_for('visualizar_produtos'))
    return render_template('cadastrar_produto.html')


@app.route('/deletar_produto/<id>', methods=['GET', 'POST'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('visualizar_produtos'))


#Rotas Trabalhador
@app.route('/visualizar_trabalhador', methods=['GET'])
def visualizar_trabalhador():
    db.create_all()
    trabalhadores = Trabalhador.query.all()
    return render_template('visualizar_trabalhador.html', trabalhadores=trabalhadores)


@app.route('/cadastrar_trabalhador', methods=['GET', 'POST'])
def cadastrar_trabalhador():
    global LIMITE_DE_TRABALHADOR
    if int(Trabalhador.query.count()) == LIMITE_DE_TRABALHADOR:
        return redirect(url_for('visualizar_trabalhador'))
    if request.method == 'POST':
        try:
            trabalhador = Trabalhador(nome=request.form['nome'], carga_horaria=request.form['carga_horaria'],
                                      custo=request.form['custo'])
            db.session.add(trabalhador)
            db.session.commit()
            return redirect(url_for('visualizar_trabalhador'))
        except:
            return redirect(url_for('cadastrar_trabalhador'))
    return render_template('cadastrar_trabalhador.html')


@app.route('/deletar_trabalhador/<id>', methods=['GET', 'POST'])
def deletar_trabalhador(id):
    trabalhador = Trabalhador.query.get(id)
    db.session.delete(trabalhador)
    db.session.commit()
    return redirect(url_for('visualizar_trabalhador'))

@app.route('/calculadora', methods=['GET'])
def calculadora():
    trabalhador = Trabalhador.query.all()
    produtos = Produto.query.all()
    return render_template('calculadora.html', trabalhador=trabalhador, produtos=produtos)

@app.route('/calcular', methods=['GET'])
def calcular():
    trabalhador = Trabalhador.query.all()
    produtos = Produto.query.all()
    return render_template('calculadora.html', trabalhador=trabalhador, produtos=produtos)

@app.route('/resultado', methods=['GET'])
def resultado():
    trabalhador = Trabalhador.query.all()
    produtos = Produto.query.all()
    return render_template('calculadora.html', trabalhador=trabalhador, produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
