import os, sys, datetime
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from colorama import Fore, Back, Style, init

app = Flask(__name__, template_folder='templates')

model = load_model(os.path.join('app', 'models', 'cifar10_model.keras'))

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
timestamp = datetime.datetime.now().isoformat()

def preprocess_image(image_file):
	img = Image.open(image_file)
	img = img.resize((32, 32))
	img = np.array(img)
	img = img / 255.0
	img = img.reshape(1, 32, 32, 3)
	return img

@app.route('/')
def index():
	return render_template('index.html',
		timestamp=datetime.datetime.now().isoformat(),
		link=request.host_url)

@app.route('/predict', methods=['POST'])
def predict():
	if request.method == 'POST':
		file = request.files['image']
		if not file:
			return render_template('index.html', prediction='No file uploaded')	
		file.save('uploaded_image.jpg')
		img = preprocess_image('uploaded_image.jpg')
		predicted = model.predict(img)	
		prediction = class_names[np.argmax(predicted)]
		print(f'predicted: {predicted}, prediction: {prediction}')
		return render_template('result.html', prediction=prediction,
	 		timestamp=datetime.datetime.now().isoformat())

if __name__ == '__main__':
	print(f'{Back.GREEN}{Style.BRIGHT}█▓▒░ START APP ░▒▓█' + Style.RESET_ALL)
	print(Back.YELLOW + Fore.BLACK + Style.BRIGHT + ' Hello, World! '+ Style.RESET_ALL)
	print(f'{Back.CYAN}{Style.BRIGHT} datetime: {datetime.datetime.now()} {Style.RESET_ALL}') 
	app.run(host='0.0.0.0', port='8080')
