from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from models import db, Utilisateur, Conversation, Message, Erreur, Solution, Outil, SolutionOutil, ErreurSolution, LogsInteraction, Requete

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fixitbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the FixItBot API'})

# Routes pour Utilisateurs
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['mdp'], method='sha256')
    new_user = Utilisateur(nom=data['nom'], email=data['email'], mdp=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = Utilisateur.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = Utilisateur.query.get_or_404(id)
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    try:
        user = Utilisateur.query.get_or_404(id)
        user.nom = data.get('nom', user.nom)
        user.email = data.get('email', user.email)
        if 'mdp' in data:
            user.mdp = generate_password_hash(data['mdp'], method='sha256')
        db.session.commit()
        return jsonify({'message': 'Utilisateur mis à jour avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Utilisateur.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Routes pour Conversations
@app.route('/conversations', methods=['POST'])
def create_conversation():
    data = request.get_json()
    new_conversation = Conversation(utilisateur_id=data['utilisateur_id'])
    try:
        db.session.add(new_conversation)
        db.session.commit()
        return jsonify({'message': 'Conversation créée avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/conversations', methods=['GET'])
def get_conversations():
    try:
        conversations = Conversation.query.all()
        return jsonify([conversation.to_dict() for conversation in conversations])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/conversations/<int:id>', methods=['GET'])
def get_conversation(id):
    try:
        conversation = Conversation.query.get_or_404(id)
        return jsonify(conversation.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/conversations/<int:id>', methods=['DELETE'])
def delete_conversation(id):
    try:
        conversation = Conversation.query.get_or_404(id)
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'message': 'Conversation supprimée avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Routes pour Messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(conversation_id=data['conversation_id'], sender=data['sender'], message=data['message'])
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message créé avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        messages = Message.query.all()
        return jsonify([message.to_dict() for message in messages])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    try:
        message = Message.query.get_or_404(id)
        return jsonify(message.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message supprimé avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Routes pour Erreurs
@app.route('/errors', methods=['POST'])
def create_error():
    data = request.get_json()
    new_error = Erreur(description=data['description'])
    try:
        db.session.add(new_error)
        db.session.commit()
        return jsonify({'message': 'Erreur créée avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/errors', methods=['GET'])
def get_errors():
    try:
        errors = Erreur.query.all()
        return jsonify([error.to_dict() for error in errors])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/errors/<int:id>', methods=['GET'])
def get_error(id):
    try:
        error = Erreur.query.get_or_404(id)
        return jsonify(error.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/errors/<int:id>', methods=['DELETE'])
def delete_error(id):
    try:
        error = Erreur.query.get_or_404(id)
        db.session.delete(error)
        db.session.commit()
        return jsonify({'message': 'Erreur supprimée avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Routes pour Solutions
@app.route('/solutions', methods=['POST'])
def create_solution():
    data = request.get_json()
    new_solution = Solution(description=data['description'])
    try:
        db.session.add(new_solution)
        db.session.commit()
        return jsonify({'message': 'Solution créée avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/solutions', methods=['GET'])
def get_solutions():
    try:
        solutions = Solution.query.all()
        return jsonify([solution.to_dict() for solution in solutions])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/solutions/<int:id>', methods=['GET'])
def get_solution(id):
    try:
        solution = Solution.query.get_or_404(id)
        return jsonify(solution.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/solutions/<int:id>', methods=['DELETE'])
def delete_solution(id):
    try:
        solution = Solution.query.get_or_404(id)
        db.session.delete(solution)
        db.session.commit()
        return jsonify({'message': 'Solution supprimée avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Routes pour Outils
@app.route('/tools', methods=['POST'])
def create_tool():
    data = request.get_json()
    new_tool = Outil(nom=data['nom'], description=data['description'])
    try:
        db.session.add(new_tool)
        db.session.commit()
        return jsonify({'message': 'Outil créé avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/tools', methods=['GET'])
def get_tools():
    try:
        tools = Outil.query.all()
        return jsonify([tool.to_dict() for tool in tools])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tools/<int:id>', methods=['GET'])
def get_tool(id):
    try:
        tool = Outil.query.get_or_404(id)
        return jsonify(tool.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tools/<int:id>', methods=['DELETE'])
def delete_tool(id):
    try:
        tool = Outil.query.get_or_404(id)
        db.session.delete(tool)
        db.session.commit()
        return jsonify({'message': 'Outil supprimé avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
