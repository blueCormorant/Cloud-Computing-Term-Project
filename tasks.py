from celery_app import Celery
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import tensorflow as tf
import logging


logging.getLogger('tensorflow').setLevel(logging.ERROR)

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = TFT5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)

app = Celery(
    "tasks",
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    CELERYD_CONCURRENCY=16
)

class Response(object):

    def __init__(self, text, filename):
        self.text = text
        self.filename = filename

@app.task
def translate_file(name, text):
    input_ids = tokenizer("translate English to French: " + text, return_tensors="tf").input_ids
    outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    filename = f"translated_{name}"
    return Response(decoded, filename).__dict__

