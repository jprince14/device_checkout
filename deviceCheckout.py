from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    devName = db.Column(db.String(64), index=True)
    devIp = db.Column(db.String(64), index=True)
    oemVer = db.Column(db.String(64), index=True)
    ver = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    user = db.Column(db.String(64), index=True)
    note = db.Column(db.String(256), index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'devName': self.devName,
            'devIp': self.devIp,
            'oemVer': self.oemVer,
            'ver': self.ver,
            'location': self.location,
            'user': self.user,
            'note': self.note,
        }


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('device_checkout.html')


@app.route('/api/data')
def data():
    query = Device.query
    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Device.devName.like(f'%{search}%'),
            Device.devIp.like(f'%{search}%'),
            Device.oemVer.like(f'%{search}%'),
            Device.ver.like(f'%{search}%'),
            Device.location.like(f'%{search}%'),
            Device.user.like(f'%{search}%'),
            Device.note.like(f'%{search}%'),
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            # Ignore the non-sortable columns
            if name in ["note"]:
                name = 'name'
            col = getattr(Device, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [device.to_dict() for device in query],
        'total': total,
    }


@app.route('/api/buttons', methods=['POST'])
def buttonsUpdate():
    data_json = request.get_json()
    field_name = data_json["field_name"]
    if field_name in ["user", "note"]:
        for device in Device.query.all():
            setattr(device, field_name, "")
    elif field_name == "add_row":
        add_row = True
        for device in Device.query.all():
            # Check if there is already a blank line
            if all(((not value) or (key == "id")) for key, value in device.to_dict().items()):
                # There is already a blank entry, do nothing
                add_row = False
                break
        if add_row:
            device = Device(devName="",
                devIp="",
                oemVer="",
                ver="",
                user="",
                location="",
                note="",)
            db.session.add(device)
    if "action" in data_json and data_json["action"] == "delete":
        Device.query.filter_by(devName=data_json["field_name"]).delete()

    db.session.commit()
    
    return '', 204


@app.route('/api/data', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    device = Device.query.get(data['id'])
    for field in ['devName', 'devIp', 'oemVer', 'ver', 'user', 'note']:
        if field in data:
            setattr(device, field, data[field])
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run()
