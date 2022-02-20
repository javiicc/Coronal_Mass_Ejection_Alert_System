from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import datetime as dt
from datetime import timedelta
from datetime import datetime
import pytz
import requests
import json
import os
import os.path as path


default_args = {
    'owner': 'javier',
#    'start_date': dt.datetime(2022, 2, 18),
    'email': 'javiercastanocandela@hotmail.com',
    'emailonfailure': True,
    'emailonretry': True,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='cme_dag2',
    schedule_interval='*/5 * * * *',  
    default_args=default_args,
    description='Coronal Mass Ejection Alert System',
    start_date=dt.datetime(2022, 2, 19, 23, 5, 00)
)


def take_event(**context):
    # Date in New York
    today = datetime.now(pytz.timezone('America/New_York')).date()
    ten_days_ago = today - timedelta(days=10)
    # Request to API, last 30 days
    try:
        # startDate: default to 30 days prior to current UTC date
        # endDate: default to current UTC date
        params = {'startDate': ten_days_ago,
                  #        'endDate': '2017-09-07'
                  }

        url = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?'
        r = requests.get(url, params)  # , params
        data = r.json()
    #   print(f'Number of CME in the 10 days prior to current date: {len(data)}')
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Something was wrong in the API request process!:(')

    # Last Event
    last_cme = data[-1]  # -1

    #path_to_activity = path.abspath(path.join('DAG2.py', "../last_100_events/{}.json".format(last_cme['activityID'])))
    path_to_activity = '/home/javier/repos/Coronal_Mass_Ejection_Alert_System/last_100_events/{}.json'.format(last_cme['activityID'])
#    new_event = False
    if os.path.exists(path_to_activity):
        print('STILL NO NEW EVENTS')
        new_event = False
        with open('/home/javier/repos/Coronal_Mass_Ejection_Alert_System/new_event.json',
                  "w") as file:
            json.dump({'new_event': 'no', 'activityID': last_cme['activityID']}, file)
    else:
        print(f"NEW EVENT: {last_cme['activityID']}")
        new_event = True
        # Save event data
        with open(path_to_activity, "w") as file:
            json.dump(last_cme, file)
        with open('/home/javier/repos/Coronal_Mass_Ejection_Alert_System/new_event.json',
                  "w") as file:
            json.dump({'new_event': 'yes', 'activityID': last_cme['activityID']}, file)

    context['task_instance'].xcom_push(key='last_cme_activity', value=last_cme['activityID'])
    context['task_instance'].xcom_push(key='new_cme_boolean', value=new_event)


take_last_event = PythonOperator(
    task_id='take_last_event',
    python_callable=take_event,
)

path_to_dashapp = path.abspath(path.join('DAG2.py', "../dashapp.py"))
dashapp = BashOperator(
    task_id='dashapp',
    bash_command=(
        'python /home/javier/repos/Coronal_Mass_Ejection_Alert_System/dashapp.py'
    ),
    dag=dag
)

kill_dashapp = BashOperator(
    task_id='kill_dashapp',
    bash_command=(
        "sleep 299 && fuser -k 3000/tcp"
    ),
    dag=dag
)

take_last_event >> [dashapp, kill_dashapp]





