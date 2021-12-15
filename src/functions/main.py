import base64
import json
from google.cloud import bigquery

def initial_method(event, context):
    #Decode pubsub message
    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        detect_sexism_message = json.loads(pubsub_message)
        print("Received message: ",str(detect_sexism_message))
        
        client = bigquery.Client()
        # TODO (developer): Set table check class
        table_id = "detection-sexist-statements.detect.sexist"
        rows_to_insert = [detect_sexism_message]
        # Make an API request
        errors = client.insert_rows_json(table_id, rows_to_insert)
        
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
        
    except Exception as e:
        print("Received message error:", e)
