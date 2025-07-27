from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import nlu
import bcrypt

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# In-memory user data
USERS = {
    'alice': {
        'password': bcrypt.hashpw('alicepass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'email': 'alice@example.com',
        'accounts': [{'type': 'savings', 'balance': 2350}],
        'cards': {'credit': {'blocked': False}, 'debit': {'blocked': False}},
        'loans': []
    }
}

# Helper to get user by username
def get_user(username):
    return USERS.get(username)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data['username'] in USERS:
        return jsonify({'msg': 'Username already exists'}), 400
    USERS[data['username']] = {
        'password': bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'email': data.get('email'),
        'accounts': [{'type': 'savings', 'balance': 0}],
        'cards': {'credit': {'blocked': False}, 'debit': {'blocked': False}},
        'loans': []
    }
    return jsonify({'msg': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = get_user(data['username'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token)
    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/loan', methods=['POST'])
@jwt_required()
def apply_loan():
    username = get_jwt_identity()
    data = request.json
    user = get_user(username)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    loan = {
        'type': data['loan_type'],
        'amount': data['amount'],
        'status': 'submitted'
    }
    user['loans'].append(loan)
    return jsonify({'msg': 'Loan application submitted'})

@app.route('/block_card', methods=['POST'])
@jwt_required()
def block_card():
    username = get_jwt_identity()
    data = request.json
    user = get_user(username)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    card = user['cards'].get(data['card_type'])
    if not card:
        return jsonify({'msg': f"{data['card_type'].title()} card not found."}), 404
    if card['blocked']:
        return jsonify({'msg': f"{data['card_type'].title()} card already blocked."}), 400
    card['blocked'] = True
    return jsonify({'msg': f"{data['card_type'].title()} card blocked successfully."})

@app.route('/account_summary', methods=['GET'])
@jwt_required()
def account_summary():
    username = get_jwt_identity()
    user = get_user(username)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    acc = user['accounts'][0]
    summary = {
        "transactions": ["-100 Grocery", "+500 Salary", "-50 Coffee", "-200 Rent", "+100 Refund"],
        "balance": f"${acc['balance']}"
    }
    return jsonify(summary)

@app.route('/conversation', methods=['POST'])
@jwt_required()
def save_conversation():
    # For demo, just acknowledge
    return jsonify({'msg': 'Conversation saved'})

@app.route('/nlu', methods=['POST'])
def nlu_parse():
    data = request.json
    result = nlu.parse(data['text'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
