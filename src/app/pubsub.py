from google.cloud import pubsub_v1

import os

def publish_new_detect_sexism(msg):
    project_id = os.environ.get('GCP_PROJECT')
    topic_id = "topic-new-detect-sexism-created"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = msg.encode('utf-8')
    future = publisher.publish(topic_path, data)
    
    print(future.result())
    print('Published message to: ', topic_path)    
    return future
    
if __name__ == '__main__':
    try:
        publish_new_detect_sexism('{ \
            "request_datetime":"2021-01-01", \
                "frase":"Why are you getting so emotional?", \
                "predict":"sexista", "proba":0.6789, }')    
    except Exception as e:
        print("pubsub error:", e)
    