from flask import Flask, request, jsonify
from utils import create_task, get_task_status, get_task_result

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the task creation API!"

@app.route('/create_task', methods=['POST'])
def create_blog_route():
    #print request.json
    print(request.json)
    data = request.json
    topic = data["topic"]
    content_type = data["content_type"]
    tonality = data["tonality"]
    content_goal = data["content_goal"]
    res = create_task(topic,content_type, tonality, content_goal)
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
    app.run(port=5000)



