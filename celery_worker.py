from celery_app import app
from tasks import translate_file

if __name__ == '__main__':
    app.worker_main()
