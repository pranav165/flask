from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from utils.get_running_env import get_running_custom_envs, AWS_ACCOUNTS
from sqlalchemy_serializer import SerializerMixin
from flask import jsonify
from time import sleep

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "super secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database\env.sqlite3'
db = SQLAlchemy(app)


class Env(db.Model, SerializerMixin):
    serialize_only = ('id', 'instance_id', 'launch_time', 'name', 'owner', 'state', 'type', 'running_since')
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(19), unique=True, nullable=False)
    launch_time = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(20), nullable=True)
    running_since = db.Column(db.Integer, default=None)

    def __init__(self, name=None, instance_id=None, launch_time=None, state=None, type=None, owner=None,
                 running_since=None):
        self.name = name
        self.instance_id = instance_id
        self.launch_time = launch_time
        self.state = state
        self.type = type
        self.owner = owner
        self.running_since = running_since

    def __repr__(self):
        return "{} {} {} {} {} {} {}".format(self.name, self.instance_id, self.launch_time,
                                             self.state, self.type, self.owner,
                                             self.running_since)


@app.route('/', methods=['GET', 'POST'])
def show_all():
    if request.method == 'POST':
        populate_running_envs()
        envs = [env.to_dict() for env in Env.query.all()]
        columns = [
            {
                'field': 'name',
                'title': 'Environment Name'
            },
            {
                'field': 'instance_id',
                'title': 'Instance ID'
            },
            {
                'field': 'launch_time',
                'title': 'Launch Time'
            },
            {
                'field': 'running_since',
                'title': 'Running Since (Days)'
            },

            {
                'field': 'type',
                'title': 'Type'
            },
            {
                'field': 'state',
                'title': 'Environment State',
                'sortable': True
            },
            {
                'field': 'owner',
                'title': 'Environment Owner'
            }
        ]
        return render_template('show_all_bootstrap.html', data=envs, columns=columns)

    return render_template('landing_page.html', enviornments=Env.query.all())


@app.route('/connected', methods=['GET', 'POST'])
def show_all_connected():
    if request.method == 'POST':
        populate_running_envs(account=AWS_ACCOUNTS.CONNECTED)
        envs = [env.to_dict() for env in Env.query.all()]
        columns = [
            {
                'field': 'name',
                'title': 'Environment Name'
            },
            {
                'field': 'instance_id',
                'title': 'Instance ID'
            },
            {
                'field': 'launch_time',
                'title': 'Launch Time'
            },
            {
                'field': 'running_since',
                'title': 'Running Since (Days)'
            },

            {
                'field': 'type',
                'title': 'Type'
            },
            {
                'field': 'state',
                'title': 'Environment State',
                'sortable': True
            },
            {
                'field': 'owner',
                'title': 'Environment Owner'
            },
        ]
        return render_template('show_all_bootstrap.html', data=envs, columns=columns)

    return render_template('landing_page.html', enviornments=Env.query.all())

# def start_env(instance_id):
#     print("Starting enviornment  --- {}".format(instance_id))
#     sleep(60)
#     print("STARTED")

# def stop_env(instance_id):
#     print("Stopping enviornment  --- {}".format(instance_id))
#     sleep(60)
#     print("Stopped")


@app.route('/start_instance', methods=['POST'])
def start_instance():
    instance_id = request.form.get('instance_id')
    return jsonify({'message': 'Instance started successfully'})

@app.route('/stop_instance', methods=['POST'])
def stop_instance():
    instance_id = request.form.get('instance_id')
    return jsonify({'message': 'Instance stopped successfully'})

@app.route('/delete_instance', methods=['POST'])
def delete_instance():
    instance_id = request.form.get('instance_id')
    # code to delete the EC2 instance with the given instance_id
    print("Deleting instance: {}".format(instance_id))
    sleep(5)
    print("Instance deleted")
    return jsonify({'message': 'Instance deleted successfully'})



def populate_running_envs(account=AWS_ACCOUNTS.DEV):
    envs = get_running_custom_envs(account=account)
    envs_db = Env.query.all()
    envs_db_id = [env["instance_id"] for env in [env.to_dict() for env in envs_db]]
    envs_id = [env["Instance"] for env in envs]
    for env_db_id in envs_db_id:
        if env_db_id not in envs_id:
            Env.query.filter_by(instance_id=env_db_id).delete()
    for env in envs:
        env_obj = Env(name=env["Name"], instance_id=env["Instance"], launch_time=env["LaunchTime"],
                      state=env["State"], type=env["Type"], owner=env["Owner"],
                      running_since=env["Running since (days)"])
        exists = db.session.query(Env.instance_id).filter_by(instance_id=env_obj.instance_id).scalar()
        if exists:
            db.session.query(Env).filter(Env.instance_id == env_obj.instance_id).update(
                {Env.running_since: env_obj.running_since,
                 Env.state: env_obj.state,
                 Env.owner: env_obj.owner}, synchronize_session=False)
            db.session.commit()
        else:
            db.session.add(env_obj)
            db.session.commit()

    return


@app.route('/api/env', methods=['GET'])
def get_enviornemnts():
    envs = Env.query.all()
    envs = [env.to_dict() for env in envs]
    return jsonify({'envs': envs})


@app.route('/api/env/pr', methods=['GET'])
def get_pr_enviornemnts():
    envs = Env.query.filter_by(pr=True).all()
    envs = [env.to_dict() for env in envs]
    return jsonify({'envs': envs})


@app.route('/api/env/e2e', methods=['GET'])
def get_e2e_enviornemnts():
    envs = Env.query.filter_by(e2e=True).all()
    envs = [env.to_dict() for env in envs]
    return jsonify({'envs': envs})


@app.route('/api/env/<env_instance_id>', methods=['GET'])
def get_enviornment(env_instance_id):
    env = Env.query.filter_by(instance_id=env_instance_id).one()
    env = env.to_dict()
    return jsonify(env)


@app.route('/api/env/<env_instance_id>', methods=['PUT'])
def update_env_e2e_status(env_instance_id):
    is_pr = request.args.get("pr")
    is_pr = True if is_pr and is_pr.lower() == 'true' else False
    is_e2e_running = request.args.get("e2e")
    is_e2e_running = True if is_e2e_running and is_e2e_running.lower() == 'true' else False
    if is_pr:
        db.session.query(Env).filter(Env.instance_id == env_instance_id).update(
            {Env.pr: True}, synchronize_session=False)
    else:
        db.session.query(Env).filter(Env.instance_id == env_instance_id).update(
            {Env.e2e: False}, synchronize_session=False)
    if is_e2e_running:
        db.session.query(Env).filter(Env.instance_id == env_instance_id).update(
            {Env.e2e: True}, synchronize_session=False)
    else:
        db.session.query(Env).filter(Env.instance_id == env_instance_id).update(
            {Env.e2e: False}, synchronize_session=False)

    db.session.commit()
    return get_enviornment(env_instance_id=env_instance_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0',port=5432)
