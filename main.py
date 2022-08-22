from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
	file = FileField("File", validators=[InputRequired()])
	submit = SubmitField("Upload File", render_kw={"onclick": "upload()"})


@app.route('/', methods=['GET',"POST"])
def home():
	form = UploadFileForm()
	if form.validate_on_submit():
		file = form.file.data # First grab the file
		file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
		
		return "File has been uploaded."
	return render_template('index.html', form=form)
	

@socketio.on('joined', namespace='/')
def handle_joining(name):
	print('joined: ' + str(name))
	emit( 'message',str(name), broadcast=True)

@socketio.on('text', namespace='/')
def handle_message(msg):
	print('message: ' + str(msg))
	emit( 'message','someone like you', broadcast=True)


if __name__ == '__main__':
	socketio.run(app, debug=True, host='192.168.1.5')
	