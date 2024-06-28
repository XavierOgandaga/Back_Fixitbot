from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    mdp = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email
        }

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'timestamp': self.timestamp
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender = db.Column(db.Enum('user', 'bot'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp
        }

class Erreur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }

class Outil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description
        }

class SolutionOutil(db.Model):
    erreur_id = db.Column(db.Integer, db.ForeignKey('erreur.id'),
                          primary_key=True, nullable=False)
    outil_id = db.Column(db.Integer, db.ForeignKey('outil.id'),
                         primary_key=True, nullable=False)
    erreur = db.relationship('Erreur', backref=db.backref('solutions_outils', lazy=True))
    outil = db.relationship('Outil', backref=db.backref('solutions_outils', lazy=True))

    def to_dict(self):
        return {
            'erreur_id': self.erreur_id,
            'outil_id': self.outil_id
            # Add more fields as needed
        }

class ErreurSolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    erreur_id = db.Column(db.Integer, db.ForeignKey('erreur.id'), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'), nullable=False)

    erreur = db.relationship('Erreur', backref=db.backref('erreurs_solutions', lazy=True))
    solution = db.relationship('Solution', backref=db.backref('erreurs_solutions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'erreur_id': self.erreur_id,
            'solution_id': self.solution_id
            # Add more fields as needed
        }

class LogsInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    utilisateur = db.relationship('Utilisateur', backref=db.backref('logs_interactions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'action': self.action,
            'timestamp': self.timestamp
            # Add more fields as needed
        }

class Requete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    utilisateur = db.relationship('Utilisateur', backref=db.backref('requetes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'description': self.description,
            'timestamp': self.timestamp
            # Add more fields as needed
        }
