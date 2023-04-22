from flask import Flask, render_template, request
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import tensorflow as tf
import logging

logging.getLogger('tensorflow').setLevel(logging.ERROR)

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = TFT5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    text = str(file.read().decode('utf-8'))
    input_ids = tokenizer("translate English to French: " + text, return_tensors="tf").input_ids  # Batch size 1
    outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded

if __name__ == '__main__':
    app.run(debug=True, port=8000)
