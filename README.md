To run the science gateway localy follow these steps:

1) Create a conda environment using the packages specified in requirements.txt and environment.yml

2) Activate the conda environment

1) Run `redis-server &`

2) Run `python app.py`

3) Run `./start_workers.sh`. Note you may need to change the number of workers or number of cores depending on your local hardware specs.

4) Go to http://localhost:8000 on your browser

5) Upload your files and wait for them to be translated. That's it!
