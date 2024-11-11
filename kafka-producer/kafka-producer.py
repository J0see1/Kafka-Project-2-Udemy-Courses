import time
import random
import csv
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

topic_name = 'udemy-courses'

dataset_path = 'dataset/udemy_courses_dataset.csv'

def quote_fields(row):
    return [f'"{field}"' if ',' in str(field) else str(field) for field in row]

with open('dataset/udemy_courses_dataset.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  

    for row in csv_reader:
        quoted_row = quote_fields(row)  
        message = ','.join(quoted_row).encode('utf-8')  
        producer.send(topic_name, message)
        print(f'Sent: {message}')    
        
        time.sleep(random.uniform(0.1, 1.0))

producer.close()
