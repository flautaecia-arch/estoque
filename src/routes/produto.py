from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.produto import Produto
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.order_by(Produto.codigo.asc()).all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos', methods=['POST'])
def create_produto():
    data = request.json
    
    try:
        validade_str = data['validade']
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        
        produto_existente = Produto.query.filter_by(
            codigo=data['codigo'],
            lote=data['lote']
        ).first()
        
        if produto_existente:
            produto_existente.quantidade += int(data['quantidade'])
            produto_existente.data_cadastro = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': f'Quantidade adicionada ao lote existente. Nova quantidade: {produto_existente.quantidade}',
                'produto': produto_existente.to_dict(),
                'acao': 'soma_quantidade'
            }), 200
        else:
            produto = Produto(
                codigo=data['codigo'],
                nome=data['nome'],
                lote=data['lote'],
                validade=validade,
                quantidade=int(data['quantidade'])
            )
            db.session.add(produto)
            db.session.commit()
            
            return jsonify({
                'message': 'Novo lote cadastrado com sucesso!',
                'produto': produto.to_dict(),
                'acao': 'novo_lote'
            }), 201
            
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Erro de integridade: Lote já existe para este produto'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao cadastrar produto: {str(e)}'}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    data = request.json
    
    try:
        produto.codigo = data.get('codigo', produto.codigo)
        produto.nome = data.get('nome', produto.nome)
        produto.lote = data.get('lote', produto.lote)
        produto.quantidade = data.get('quantidade', produto.quantidade)
        
        if 'validade' in data:
            validade_str = data['validade']
            produto.validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify(produto.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar produto: {str(e)}'}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return '', 204

@produto_bp.route('/produtos/resumo', methods=['GET'])
def get_resumo_estoque():
    """
    Retorna um resumo do estoque agrupado por código do produto,
    somando as quantidades independente do lote
    """
    resumo = db.session.query(
        Produto.codigo,
        Produto.nome,
        func.sum(Produto.quantidade).label('quantidade_total'),
        func.count(Produto.id).label('total_lotes')
    ).group_by(Produto.codigo, Produto.nome).order_by(Produto.codigo.asc()).all()
    
    resultado = []
    for item in resumo:
        resultado.append({
            'codigo': item.codigo,
            'nome': item.nome,
            'quantidade_total': item.quantidade_total,
            'total_lotes': item.total_lotes
        })
    
    return jsonify(resultado)

@produto_bp.route('/produtos/por-codigo/<codigo>', methods=['GET'])
def get_produtos_por_codigo(codigo):
    """
    Retorna todos os produtos de um código específico (diferentes lotes)
    """
    produtos = Produto.query.filter_by(codigo=codigo).order_by(Produto.validade.asc()).all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos/adicionar-lote', methods=['POST'])
def adicionar_lote():
    """
    Adiciona um novo lote a um produto existente ou cria um novo produto
    """
    data = request.json
    
    try:
        validade_str = data['validade']
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        
        produto_existente = Produto.query.filter_by(
            codigo=data['codigo'],
            lote=data['lote']
        ).first()
        
        if produto_existente:
            produto_existente.quantidade += int(data['quantidade'])
            produto_existente.data_cadastro = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': f'Quantidade adicionada ao lote existente. Nova quantidade: {produto_existente.quantidade}',
                'produto': produto_existente.to_dict(),
                'acao': 'soma_quantidade'
            }), 200
        else:
            produto = Produto(
                codigo=data['codigo'],
                nome=data['nome'],
                lote=data['lote'],
                validade=validade,
                quantidade=int(data['quantidade'])
            )
            db.session.add(produto)
            db.session.commit()
            
            return jsonify({
                'message': 'Novo lote adicionado com sucesso!',
                'produto': produto.to_dict(),
                'acao': 'novo_lote'
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao adicionar lote: {str(e)}'}), 500

@produto_bp.route('/produtos/limpar-todos', methods=['DELETE'])
def limpar_todos_produtos():
    """
    Remove todos os produtos do banco de dados.
    ATENÇÃO: Esta operação é irreversível!
    """
    try:
        total_produtos = Produto.query.count()
        
        Produto.query.delete()
        db.session.commit()
        
        return jsonify({
            'message': f'Todos os dados foram limpos com sucesso! {total_produtos} lote(s) removido(s).',
            'produtos_removidos': total_produtos
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Erro ao limpar dados: {str(e)}'
        }), 500



