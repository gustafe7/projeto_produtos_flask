import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Criar app Flask
app = Flask(__name__)

# Caminho absoluto da pasta do app
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco de dados
db = SQLAlchemy(app)

# Modelo de Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Criar tabelas
with app.app_context():
    db.create_all()

# Rota da página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'preco': p.preco} for p in produtos])

# Rota para criar produto
@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')
    if not nome or preco is None:
        return jsonify({'error': 'Dados incompletos'}), 400
    try:
        preco = float(preco)
    except ValueError:
        return jsonify({'error': 'Preço inválido'}), 400

    produto = Produto(nome=nome, preco=preco)
    db.session.add(produto)
    db.session.commit()
    return jsonify({'id': produto.id, 'nome': produto.nome, 'preco': produto.preco}), 201

    # Rota para excluir produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    try:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'sucesso': 'Produto excluído'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': 'Erro ao excluir produto'}), 500

# Rodar app
if __name__ == '__main__':
    app.run(debug=True)
