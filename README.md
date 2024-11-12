# Project 2 Kafka-Spark
## Big Data Streaming System for Udemy Course Clustering

| Nama                            | NRP          |
| ------------------------------- | ------------ |
| Marcelinus Alvinanda Chrisantya | `5027221012` |
| Etha Felisya Br Purba           | `5027221017` |
| Fazrul Ahmad Fadhilah           | `5027221025` |

## Project Overview
Proyek ini mengimplementasikan sistem Big Data streaming menggunakan **Apache Kafka** dan **Apache Spark** untuk simulasi pemrosesan data stream dan pelatihan model clustering. Dataset yang digunakan adalah data kursus Udemy dengan tujuan mengelompokkan kursus berdasarkan metrik tertentu, seperti popularitas, tingkat kesulitan, dan tren waktu.

## Dataset
Dataset yang digunakan mencakup informasi berikut:
- **course_id**: ID unik untuk setiap kursus.
- **course_title**: Judul kursus.
- **url**: Link langsung ke kursus di Udemy.
- **is_paid**: Status berbayar atau gratis.
- **price**: Harga kursus (jika berbayar).
- **num_subscribers**: Jumlah subscriber kursus.
- **num_reviews**: Jumlah review dari peserta kursus.
- **num_lectures**: Jumlah lecture dalam kursus.
- **level**: Tingkat kesulitan kursus (Beginner, Intermediate, Expert).
- **content_duration**: Durasi total konten kursus dalam jam.
- **published_timestamp**: Waktu publikasi kursus di Udemy.
- **subject**: Kategori utama kursus (misalnya, Bisnis, Teknologi).


## Clustering Models
Proyek ini menghasilkan tiga model clustering menggunakan fitur yang berbeda. Berikut adalah deskripsi model yang dibuat:
### 1. Clustering Berdasarkan Popularitas dan Engagement Kursus
   - **Fitur**: `num_subscribers`, `num_reviews`, `num_lectures`, `content_duration`
   - **Tujuan**: Mengelompokkan kursus berdasarkan popularitas dan tingkat engagement.
   - **Penggunaan**: Mengidentifikasi kursus yang sangat populer dan menganalisis faktor-faktor yang membuatnya menonjol.

### 2. Clustering Berdasarkan Tingkat Kesulitan dan Konten Kursus
   - **Fitur**: `level`, `num_lectures`, `content_duration`
   - **Tujuan**: Mengelompokkan kursus berdasarkan tingkat kesulitan dan kedalaman konten.
   - **Penggunaan**: Membantu mengkategorikan kursus ke dalam kelompok pemula, menengah, dan lanjutan.

### 3. Clustering Berdasarkan Tren Waktu untuk Kursus
   - **Fitur**: `published_timestamp`, `num_subscribers`, `num_reviews`
   - **Tujuan**: Mengelompokkan kursus berdasarkan tren waktu untuk memahami popularitas kursus dalam kurun waktu tertentu.
   - **Penggunaan**: Mengungkap tren pada topik-topik yang populer atau menurun.



## Workflow

1. **Docker Setup**: 
   - File `docker-compose.yaml` digunakan untuk menjalankan kontainer Kafka, Zookeeper, dan layanan pendukung lainnya.

2. **Kafka Producer**:
   - File `kafka-producer.py` di dalam folder `kafka-producer` membaca dataset (`udemy_courses_dataset.csv`) secara sekuensial dan mengirim data baris demi baris ke Kafka server dengan jeda acak, untuk mensimulasikan proses streaming.
   - Dataset diproses dan dibagi menjadi tiga batch (`batch_1.csv`, `batch_2.csv`, `batch_3.csv`) yang disimpan di folder `dataset/batch-dataset`.

3. **Kafka Consumer**:
   - File `kafka-consumer.py` di dalam folder `kafka-consumer` membaca data dari Kafka server dan menyimpannya ke dalam batch sesuai dengan konfigurasi yang ditentukan.

4. **Model Training**:
   - Model KMeans dilatih menggunakan Spark berdasarkan batch data yang telah disimpan.
   - Tiga notebook (`model-1.ipynb`, `model-2.ipynb`, `model-3.ipynb`) berisi proses pelatihan model Spark KMeans untuk masing-masing batch. Model yang dihasilkan disimpan di folder `kafka-model`:
     - `spark_kmeans_model_a`: Hasil pelatihan model untuk batch pertama.
     - `spark_kmeans_model_b`: Hasil pelatihan model untuk batch kedua.
     - `spark_kmeans_model_c`: Hasil pelatihan model untuk batch ketiga.

5. **API Development**:
   - File `api.py` digunakan untuk mengimplementasikan API yang menyediakan endpoint untuk setiap model clustering. Endpoint ini menerima input dari pengguna dan memberikan hasil clustering sesuai model yang dilatih.

## API Endpoints

1. **Endpoint 1: `/course_popularity`**
   - Menggunakan fitur `num_subscribers`, `num_reviews`, `num_lectures`, dan `content_duration` sebagai input.
   - Contoh permintaan:
     ```bash
     curl -X POST "http://127.0.0.1:5000/course_popularity" -H "Content-Type: application/json" -d '{
       "num_subscribers": "10000",
       "num_reviews": "150",
       "num_lectures": "30",
       "content_duration": "5.0"
     }'
     ```

2. **Endpoint 2: `/course_difficulty`**
   - Menggunakan fitur `num_subscribers`, `num_reviews`, `num_lectures`, dan `content_duration` sebagai input.
   - Contoh permintaan:
     ```bash
     curl -X POST "http://127.0.0.1:5000/course_difficulty" -H "Content-Type: application/json" -d '{
       "num_subscribers": "5000",
       "num_reviews": "100",
       "num_lectures": "20",
       "content_duration": "2.5"
     }'
     ```

3. **Endpoint 3: `/course_price_analysis`**
   - Menggunakan fitur `price`, `num_subscribers`, `num_reviews`, dan `content_duration` sebagai input.
   - Contoh permintaan:
     ```bash
     curl -X POST "http://127.0.0.1:5000/course_price_analysis" -H "Content-Type: application/json" -d '{
       "price": "200.0",
       "num_subscribers": "1500",
       "num_reviews": "200",
       "content_duration": "3.5"
     }'
     ```

## How to Run the Project

1. **Start Docker Services**:
   - Jalankan perintah berikut untuk memulai Kafka dan layanan terkait.
     ```bash
     docker-compose up -d
     ```

2. **Run Kafka Producer**:
   - Eksekusi `kafka-producer.py` untuk mengirim data secara streaming ke Kafka.
   
3. **Run Kafka Consumer**:
   - Jalankan `kafka-consumer.py` untuk membaca data dari Kafka dan menyimpannya sebagai batch.

4. **Train Models**:
   - Jalankan masing-masing notebook (`model-1.ipynb`, `model-2.ipynb`, `model-3.ipynb`) untuk melatih model berdasarkan batch data yang sudah dibuat.

5. **Start API Server**:
   - Jalankan `api.py` untuk memulai server API yang menyediakan endpoint untuk setiap model clustering.

