import time
import random
import csv
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

topic_name = 'udemy-courses'

with open('dataset/udemy_courses_dataset.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader) 

    for row in csv_reader:
        message = ','.join(row).encode('utf-8')  
        producer.send(topic_name, message)
        print(f'Sent: {message}')
        
        time.sleep(5)

producer.close()