from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
db = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/test', methods=['GET'])
def test_connection():
    try:
        db.ping()
        return jsonify({'message': 'Polaczono z baza Redis'}), 200
    except redis.exceptions.ConnectionError as e:
        return jsonify({'error': 'Nie można polaczyc się z baza Redis'}), 500


@app.route('/resource', methods=['POST'])
def create_resource():
    data = request.json
    if 'key' not in data or 'value' not in data:
        return jsonify({'error': 'Brak wymaganych pol'}), 400

    key = data['key']
    value = data['value']

    if db.exists(key):
        return jsonify({'error': 'Zasob już istnieje'}), 400

    db.set(key, value)
    return jsonify({'message': 'Zasob został utworzony'}), 201


@app.route('/resource/<string:key>', methods=['GET'])
def read_resource(key):
    value = db.get(key)
    if value is None:
        return jsonify({'error': 'Zasob nie istnieje'}), 404

    return jsonify({'key': key, 'value': value.decode('utf-8')}), 200


@app.route('/resource', methods=['GET'])
def get_all_resources():
    keys = db.keys('*')  # Pobieramy wszystkie klucze w bazie Redis
    resources = []

    for key in keys:
        value = db.get(key)
        resources.append({'key': key.decode('utf-8'), 'value': value.decode('utf-8')})

    return jsonify(resources), 200


@app.route('/resource/<string:key>', methods=['PUT'])
def update_resource(key):
    data = request.json
    if 'value' not in data:
        return jsonify({'error': 'Brak wymaganych pol'}), 400

    value = data['value']

    if not db.exists(key):
        return jsonify({'error': 'Zasob nie istnieje'}), 404

    db.set(key, value)
    return jsonify({'message': 'Zasob został zaktualizowany'}), 200


@app.route('/resource/<string:key>', methods=['DELETE'])
def delete_resource(key):
    if not db.exists(key):
        return jsonify({'error': 'Zasob nie istnieje'}), 404

    db.delete(key)
    return jsonify({'message': 'Zasob został usuniety'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
