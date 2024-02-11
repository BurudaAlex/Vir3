from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from database_setup import PassesDB
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


# Загрузка переменных окружения из файла .env
load_dotenv()

# Создание экземпляра класса PassesDB с использованием значений из конфигурации
db = PassesDB(
    host=os.getenv("FSTR_DB_HOST"),
    database=os.getenv("FSTR_DB_DATABASE"),
    user=os.getenv("FSTR_DB_USER"),
    password=os.getenv("FSTR_DB_PASSWORD")
)

app = Flask(__name__)

@app.route('/submitData', methods=['POST'])
def submit_data():
    data = request.json
    result = db.submit_data(data)
    return jsonify(result)

@app.route('/submitData/<int:id>', methods=['GET'])
def get_data(id):
    data = db.get_data_by_id(id)
    if data:
        return jsonify(data)
    else:
        return jsonify({'message': 'Ошибка при получении данных'})

@app.route('/submitData/<int:id>', methods=['PATCH'])
def edit_data(id):
    data = request.json
    result = db.edit_data_by_id(id, data)
    return jsonify(result)

@app.route('/submitData/', methods=['GET'])
def get_data_by_email():
    email = request.args.get('user__email')
    data = db.get_data_by_email(email)
    if data:
        return jsonify(data)
    else:
        return jsonify({'message': 'Ошибка при получении данных'})

if __name__ == '__main__':
    app.run(debug=True)
