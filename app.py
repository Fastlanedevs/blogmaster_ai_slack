from flask import Flask, request, jsonify
from utils import create_task, get_task_status, get_task_result

app = Flask(__name__)

@app.route('/create_task', methods=['POST'])
def create_blog_route():
    data = request.json
    topic = data["topic"]
    res = create_task(topic)
    return jsonify({"task_id": res})

@app.route('/get_task_status/<string:id>', methods=['GET'])
def get_task_status_route(id):
    res = get_task_status(id)
    return jsonify({"task_status": res})

@app.route('/get_task_result/<string:id>', methods=['GET'])
def get_task_result_route(id):
    res = get_task_result(id)
    return jsonify(res)

    

if __name__ == '__main__':
    app.run(port=8000)



