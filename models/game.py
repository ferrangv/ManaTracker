from datetime import datetime
from models import db

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    colors = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    sr_turn1 = db.Column(db.Boolean)
    result = db.Column(db.String(50))
    turns = db.Column(db.Integer)
    end_condition = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='games')
