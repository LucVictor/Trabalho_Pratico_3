#Importação de bibliotecas
import os  #Biblioteca de acesso a arquivos do sistema operacional.
from flask import Flask, render_template, request, url_for, redirect  #Biblioteca flask
from flask_sqlalchemy import SQLAlchemy  #Biblioteca ORM sqlalchemy para flask
from app.gauss import eliminacao_gauss_jordan

app = Flask(__name__)  #Definição de aplicação flask
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URL', 'mysql+pymysql://usuario:password@endereco/banco')  # Definição do tipo de banco e nome do arquivo do banco.
db = SQLAlchemy(app)

#Variáveis constantes globais de limite
LIMITE_DE_TRABALHADOR = 2  #Limite definido pelo modelo
LIMITE_DE_PRODUTOS = 3  #Limite definido pelo modelo

def quantidade_de_trabalhador(): #Função que retorna o número de trabalhadores no banco de dados
    quantidade = Trabalhador.query.count()
    return int(quantidade)

def quantidade_de_produtos(): #Função que retorna o número de produtos no banco de dados
    quantidade = Produto.query.count()
    return int(quantidade)

def converter_decimal_para_horas(decimal): #Função para converter decimal para horas
    horas = int(decimal)
    minutos = round((decimal - horas) * 60)
    return f'{horas:02d}:{minutos:02d}h'

def converter_tempo_para_decimal(tempo): #Função para converter horas para decimal
    tempo = tempo.replace('h', '').strip()
    horas, minutos = map(int, tempo.split(':'))
    horas_decimais = horas + minutos / 60
    return horas_decimais


def formatar_para_salvar(trabalhador, tempos, produtos): #Função para formatar os dados inseridos na tela de cálculo.
    texto = []
    for i in range(len(produtos)):
        texto.append(f"{trabalhador.nome} produz o {produtos[i].nome} em {converter_decimal_para_horas(tempos[i])}.")
    return "\n".join(texto)


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
    produto_1 = db.Column(db.String(250), nullable=False)
    produto_2 = db.Column(db.String(250), nullable=False)
    produto_3 = db.Column(db.String(250), nullable=False)
    produto_1_quantidade = db.Column(db.Float, nullable=False)
    produto_2_quantidade = db.Column(db.Float, nullable=False)
    produto_3_quantidade = db.Column(db.Float, nullable=False)
    lucratividade = db.Column(db.Float, nullable=False)
    custos_adicionais = db.Column(db.Float, nullable=False)
    tempos = db.Column(db.Text(10000), nullable=False)


@app.route('/', methods=['GET']) #Rota que exibe página principal
def index():
    return render_template('index.html')


#Rotas Produtos
@app.route('/visualizar_produtos', methods=['GET']) #Rota que exibe os produtos.
def visualizar_produtos():
    produtos = Produto.query.all() #Busca todos os produtos do banco de dados.
    return render_template('/visualizar_produtos.html', produtos=produtos)


@app.route('/cadastrar_produto', methods=['GET', 'POST']) #Rota para cadastro de produtos.
def cadastro_produto():
    global LIMITE_DE_PRODUTOS #Importa a variável constante para dentro do escopo da função
    if int(Produto.query.count()) == LIMITE_DE_PRODUTOS: #Bloqueia o acesso caso o número de produtos seja igual ao limite.
        return redirect(url_for('visualizar_produtos')) #Redireciona para a página de exibir produtos.
    if request.method == 'POST':
        try: #Tenta realizar o cadastro
            produto = Produto(nome=request.form['nome'], rentabilidade=request.form['rentabilidade']) #Criação do objeto produto, recebe nome e rentabilidade do formulário.
            db.session.add(produto)#Coloca o objeto produto na fila.
            db.session.commit() #Salva o produto no bando de dados.
            return redirect(url_for('visualizar_produtos')) #Redireciona para a página de exibir produtos.
        except: #Caso aconteça algum erro
            return redirect(url_for('visualizar_produtos'))  #Redireciona para a página de exibir produtos.
    return render_template('/cadastrar_produto.html')


@app.route('/deletar_produto/<int:produto_id>', methods=['GET', 'POST']) #Rota que deleta produtos cadastrados.
def deletar_produto(produto_id):
    produto = Produto.query.get(produto_id) #Recebe o id do produto.
    db.session.delete(produto) #Coloca o objeto produto na fila.
    db.session.commit() #Deleta o produto do banco de dados.
    return redirect(url_for('visualizar_produtos')) #Redireciona para a página de exibir produtos.


#Rotas Trabalhador
@app.route('/visualizar_trabalhador', methods=['GET'])  #Rota que exibe os produtos.
def visualizar_trabalhador():
    trabalhadores = Trabalhador.query.all()  #Busca todos os produtos do banco de dados.
    return render_template('/visualizar_trabalhador.html', trabalhadores=trabalhadores)


@app.route('/cadastrar_trabalhador', methods=['GET', 'POST']) #Rota para cadastro de trabalhadores.
def cadastrar_trabalhador():
    global LIMITE_DE_TRABALHADOR #Importa a variável constante para dentro do escopo da função
    if int(Trabalhador.query.count()) == LIMITE_DE_TRABALHADOR:  #Bloqueia o acesso caso o número de trabalhadores seja igual ao limite.
        return redirect(url_for('visualizar_trabalhador')) #Redireciona para a página de exibir trabalhadores.
    if request.method == 'POST':
        try: #Tenta realizar o cadastro
            trabalhador = Trabalhador(nome=request.form['nome'], carga_horaria=request.form['carga_horaria'],
                                      custo=request.form['custo'])  #Criação do objeto trabalhador, recebe nome e carga e custo.
            db.session.add(trabalhador)
            db.session.commit()
            return redirect(url_for('visualizar_trabalhador')) #Redireciona para a página de exibir trabalhadores.
        except: #Caso aconteça algum erro
            return redirect(url_for('cadastrar_trabalhador')) #Redireciona para a página de exibir trabalhadores.
    return render_template('/cadastrar_trabalhador.html')


@app.route('/deletar_trabalhador/<int:trabalhador_id>', methods=['GET', 'POST'])  #Rota que deleta trabalhadores cadastrados.
def deletar_trabalhador(trabalhador_id):
    trabalhador = Trabalhador.query.get_or_404(trabalhador_id)  #Recebe o id do trabalhador.
    db.session.delete(trabalhador) #Coloca o objeto trabalhador na fila.
    db.session.commit()  #Deleta o trabalhador do banco de dados.
    return redirect(url_for('visualizar_trabalhador')) #Redireciona para a página de exibir trabalhador.

@app.route('/calculadora', methods=['GET']) #Rota para preenchimento do formulário de tempo
def calculadora():
    trabalhador = Trabalhador.query.all() #Busca todos os trabalhadores do banco de dados
    produtos = Produto.query.all() #Busca todos os produtos do banco de dados
    if quantidade_de_produtos() == LIMITE_DE_PRODUTOS and quantidade_de_trabalhador() == LIMITE_DE_TRABALHADOR: #Verifica se a calculadora está com os cadastros confome definida.
        return render_template('/calculadora.html', trabalhador=trabalhador, produtos=produtos)
    return render_template('erro.html', e="A calculadora não possui 2 de trabalhadores e 3 produtos cadastrados.")


@app.route('/calcular', methods=['POST']) #Rota responsável pelo cálculo
def calcular():
    form = request.form.getlist("tempo") #Recebe todos os dados de tempo do formulário
    matriz = [] #Criação da matriz para inicial.
    for i in form: #Pecorre cada item que existe na variável que contém os tempos
        conversao_decimal = converter_tempo_para_decimal(i)
        matriz.append(conversao_decimal) #Adiciona o tempo convertido em horas para a matriz inicial.

    metade = len(matriz) // quantidade_de_trabalhador() #Divisão da quantidade de itens da matriz pelo número de trabalhadores
    matriz_linha_1 = matriz[:metade] #Linha 1 referente ao trabalhador 1(exemplo: Artesão)
    matriz_linha_2 = matriz[metade:] #Linha 2 referente ao trabalhador 2(exemplo: Coletor)
    matriz_linha_3 = [0, 0, 1] #Defenido pelo número mínimo de quadros a ser produzido.
    matriz_convertida = matriz_linha_1, matriz_linha_2, matriz_linha_3 #Matriz final contendo as 3 linhas.

    restricoes=[] #Criação da matriz de restrição
    for i in Trabalhador.query.all(): #Pecorre todos os trabalhadores cadastrados.
        restricoes.append(i.carga_horaria) #Adiciona somente a carga horária de cadas trabalhador a matriz de restrição.

    quadros_minimos = request.form["quadros_ninimos"] #Recebe o número de quadros mínimo do formulário.
    custos_adicionais = int(request.form["custos_adicionais"])
    restricoes.append(int(quadros_minimos)) #Adiciona a restrições o número mínimo de quadros a serem produzidos.
    try: #tenta realizar o cálculo chamando o algoritmo de resolução.
        resultado = eliminacao_gauss_jordan(matriz_convertida, restricoes) #Envia as duas matrizes ao algoritmo de resolução de gauss jordan.
        produtos = Produto.query.all() #Lista todos os produtos do banco de dados.
        trabalhadores = Trabalhador.query.all()#Lista todos os trabalhadores do bando de dados.

        lucro = produtos[0].rentabilidade * resultado[0] + produtos[1].rentabilidade * resultado[1] + produtos[2].rentabilidade * resultado[2]
        #Calcula a soma dos lucros de cada item, Produto.rentabilidade * Resultado(Quantidade a ser produzida do produto)

        custo = trabalhadores[0].custo + trabalhadores[1].custo  #Soma todos os custos de todos os trabalhadores do banco de dados.

        balanco = lucro - custo - custos_adicionais #Soma o lucro com os custos

        descricao_trabalhador_1 = formatar_para_salvar(trabalhadores[0], matriz_linha_1, produtos) #Chama a função para formatar o texto a ser salvo.
        descricao_trabalhador_2 = formatar_para_salvar(trabalhadores[1], matriz_linha_2, produtos) #Chama a função para formatar o texto a ser salvo.

        descricao_final = f"{descricao_trabalhador_1}\n\n{descricao_trabalhador_2}" #Adiciona as duas descrições de cálculos a variável a ser salva.
        salvar_resultado = Resultados(produto_1=produtos[0].nome, produto_2=produtos[1].nome, produto_3=produtos[2].nome,
                                      produto_1_quantidade=resultado[0], produto_2_quantidade=resultado[1],
                                      produto_3_quantidade=resultado[2], lucratividade=balanco, tempos=descricao_final, custos_adicionais=custos_adicionais)
        #Salva o resultado no banco de dados
        db.session.add(salvar_resultado) #Adiciona o objeto resultado no fila.
        db.session.commit() #Grava o resultado no banco de dados.
    except ValueError as e: #Caso o algoritmo retorne algum erro, será exibido na tela de erro.
        return render_template('erro.html', e=e)

    return redirect(url_for('resultados')) #Redireciona para página de resultados


@app.route('/resultados', methods=['GET']) #Rota que exibe os resultados.
def resultados():
    resultado = Resultados.query.order_by(Resultados.id.desc()).all() #Busca todos os resultados do banco de dados.
    tamanho = len(resultado) #Calcula a quantidade de resultados.
    return render_template('/resultado.html', resultados=resultado, tamanho=tamanho)


@app.route('/erro', methods=['GET']) #Rota que exibe os resultados.
def erro():
    return render_template('/erro.html')