from time import sleep
from q_tasks.celery_main import celery_main


@celery_main.task
def hello(name='hello'):
    sleep(15)
    print (f'{name} pidor!')

