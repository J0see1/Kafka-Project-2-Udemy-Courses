import time
import random
import csv
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

topic_name = 'udemy-courses'

with open('dataset/udemy_courses_dataset.csv', 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  

    for row in csv_reader:
        message = ','.join(row).encode('utf-8')  
        producer.send(topic_name, message)
        print(f'Sent: {message}')
        
    time.sleep(random.uniform(0.1, 1.0))

producer.close()
