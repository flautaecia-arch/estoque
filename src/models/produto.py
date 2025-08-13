from src.models.user import db
from datetime import datetime

class Produto(db.Model):
    """
    Modelo para armazenar lotes específicos de produtos.
    Cada lote é identificado por um código de produto e um número de lote.
    """
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice único para evitar lotes duplicados (mesmo código + lote)
    __table_args__ = (
        db.UniqueConstraint('codigo', 'lote', name='unique_codigo_lote'),
    )

    def __repr__(self):
        return f'<Produto {self.codigo} - Lote {self.lote}: {self.quantidade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'lote': self.lote,
            'validade': self.validade.isoformat() if self.validade else None,
            'quantidade': self.quantidade,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
        }


