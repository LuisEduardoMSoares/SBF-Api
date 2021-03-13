import sqlalchemy as db

from ...db.engine import Base


ProductProvider = db.Table('association_products_providers', Base.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('base_products.id')),
    db.Column('provider_id', db.Integer, db.ForeignKey('base_providers.id')),
    
    # Place an index on product_id and provider_id
    db.Index('only_one_association', 'product_id', 'provider_id', unique=True),
)