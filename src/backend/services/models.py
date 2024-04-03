from services.database import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)
        
    @classmethod
    def authenticate(cls, name: str, password: str):
        user = cls.query.filter_by(name=name).first()
        if not user:
            raise Exception("User does not exist")
        if not check_password_hash(user.password, password):
            raise Exception("Incorrect password")
        
        return user
    
    @classmethod
    def register(cls, name: str, password: str):
        user = cls.query.filter_by(name=name).first()
        if user is not None:
            raise Exception("User already exists. Please, log in.")
        
        user = User(name, password)
        db.session.add(user)
        db.session.commit()
        return user
        

    def to_dict(self):
        return dict(id=self.id, name=self.name)
    
    def __repr__(self):
        return f"<User {self.name}>"