#Importação de bibliotecas
import os  #Biblioteca de acesso a arquivos do sistema operacional.
from flask import Flask, render_template, request, url_for, redirect, flash  #Biblioteca flask
from flask_sqlalchemy import SQLAlchemy  #Biblioteca ORM sqlalchemy para flask
from gauss import eliminacao_gauss_jordan

basedir = os.path.abspath(os.path.dirname(__file__))  #Definição do caminho(path) raíz(root)
app = Flask(__name__)  #Definição de aplicação flask
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(basedir, 'database.db'))  # Definição do tipo de banco e nome do arquivo do banco.
db = SQLAlchemy(app)

#Variáveis constantes globais de limite
LIMITE_DE_TRABALHADOR = 2  #Limite definido pelo modelo
LIMITE_DE_PRODUTOS = 3  #Limite defenido pelo modelo

def quantidade_de_trabalhador():
    quantidade = Trabalhador.query.count()
    return int(quantidade)

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

class Resultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_1 = db.Column(db.String, nullable=False)
    produto_2 = db.Column(db.String, nullable=False)
    produto_3 = db.Column(db.String, nullable=False)
    produto_1_quantidade = db.Column(db.Float, nullable=False)
    produto_2_quantidade = db.Column(db.Float, nullable=False)
    produto_3_quantidade = db.Column(db.Float, nullable=False)
    lucratividade = db.Column(db.Float, nullable=False)



#Rotas Produtos
@app.route('/visualizar_produtos', methods=['GET'])
def visualizar_produtos():
    db.create_all()
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

@app.route('/calcular', methods=['POST'])
def calcular():
    form = request.form.getlist("tempo")
    matriz = []
    for i in form:
        hora, minuto = i.split(":")
        conversao_hora = int(hora) + (int(minuto) / 60)
        matriz.append(conversao_hora)
    metade = len(matriz) // quantidade_de_trabalhador()
    matriz_linha_1 = matriz[:metade]
    matriz_linha_2 = matriz[metade:]
    matriz_linha_3 = [0, 0, 1]
    matriz_convertida = matriz_linha_1, matriz_linha_2, matriz_linha_3

    restricoes=[]
    for i in Trabalhador.query.all():
        restricoes.append(i.carga_horaria)

    quadros_minimos = request.form["quadros_ninimos"]
    restricoes.append(int(quadros_minimos))

    resultado = eliminacao_gauss_jordan(matriz_convertida, restricoes)
    produtos = Produto.query.all()
    trabalhadores = Trabalhador.query.all()
    lucro = produtos[0].rentabilidade * resultado[0] + produtos[1].rentabilidade * resultado[1] + produtos[2].rentabilidade * resultado[2]
    custo = trabalhadores[0].custo + trabalhadores[1].custo
    balanco = lucro - custo

    salvar_resultado = Resultados(produto_1=produtos[0].nome, produto_2=produtos[1].nome, produto_3=produtos[2].nome,
                                  produto_1_quantidade=resultado[0], produto_2_quantidade=resultado[1],
                                  produto_3_quantidade=resultado[2], lucratividade=balanco)
    db.session.add(salvar_resultado)
    db.session.commit()

    return redirect(url_for('resultados'))


@app.route('/resultados', methods=['GET'])
def resultados():
    resultados = Resultados.query.all()
    tamanho = len(resultados)
    return render_template('resultado.html', resultados=resultados, tamanho=tamanho)

if __name__ == "__main__":
    app.run(debug=True)
