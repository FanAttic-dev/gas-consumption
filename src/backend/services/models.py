from app import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password, method='sha256')
        
    @classmethod
    def authenticate(cls, **kwargs):
        name = kwargs.get('name')
        password = kwargs.get('password')
        
        if not name or not password:
            return None
        
        user = cls.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user

    def to_dict(self):
        return dict(id=self.id, name=self.name)
    
    def __repr__(self):
        return f"<User {self.name}>"