from kafka import KafkaConsumer
import os

consumer = KafkaConsumer(
    'udemy-courses',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='batch_consumer'
)

batch_size = 1193  
batch = []
batch_count = 1
output_dir = 'dataset/batch-dataset'

os.makedirs(output_dir, exist_ok=True)

for message in consumer:
    batch.append(message.value.decode('utf-8'))

    if len(batch) >= batch_size:
        with open(f'{output_dir}/batch_{batch_count}.csv', 'w', encoding='utf-8') as f:
            f.write('\n'.join(batch))
        print(f'Saved batch {batch_count} with {len(batch)} records')
        
        batch = []
        batch_count += 1

#  jika ada sisa data maka akan dimasukin ke batch terakhir
if batch:
    with open(f'{output_dir}/batch_{batch_count}.csv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(batch))
    print(f'Saved batch {batch_count} with {len(batch)} records')

consumer.close()
