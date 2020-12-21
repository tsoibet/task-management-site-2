import time
from flask import Flask, abort, jsonify, request

from database import init_db, db
from model.models import Status, Task, TaskSchema, CreateTaskInputSchema, QueryTaskInputSchema

from marshmallow import ValidationError
from sqlalchemy import func

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run()


@app.route('/')
def hello():
    return jsonify({'status': 'ok', 'server_time': time.strftime("%m/%d/%Y, %H:%M:%S")})


@app.route('/status')
def get_status():
    return jsonify([Status.TO_DO.name, Status.IN_PROGRESS.name, Status.DONE.name])

@app.route('/tasks')
def get_tasks():
    try:
        query = QueryTaskInputSchema().load(request.args)
    except ValidationError as err:
        return jsonify({'status': 'nok', 'message': err.messages})
    if query['sort'] == 'priority':
        results = Task.query.order_by(Task.priority).order_by(Task.status).order_by(
            Task.deadline).paginate(query['page'], query['per'], False)
    elif query['sort'] == 'deadline':
        results = Task.query.order_by(Task.deadline).order_by(Task.status).order_by(
            Task.priority).paginate(query['page'], query['per'], False)
    else:
        results = Task.query.order_by(Task.status).order_by(Task.priority).order_by(
            Task.deadline).paginate(query['page'], query['per'], False)
    total = results.total
    tasks = results.items
    return jsonify({'status': 'ok', 'total': total, 'tasks': TaskSchema(many=True).dump(tasks)})


@app.route('/task/<int:id>')
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({'status': 'ok', 'tasks': TaskSchema().dump(task)})

@app.route('/task', methods=['POST'])
def new_task():
    try:
        result = CreateTaskInputSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({'status': 'nok', 'message': err.messages})
    db.session.add(result)
    db.session.commit()
    return jsonify({'status': 'ok', 'task': TaskSchema().dump(result)})


@app.route('/task/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return abort(404)
    data = request.get_json()
    err = CreateTaskInputSchema().validate(data)
    if err:
        return jsonify({'status': 'nok', 'message': err})
    task.update_dict(data)
    db.session.commit()
    return jsonify({'status': 'ok', 'task': TaskSchema().dump(task)})

@app.route('/task/del/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'status': 'ok', 'id': id})

