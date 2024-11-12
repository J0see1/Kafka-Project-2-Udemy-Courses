from flask import Flask, request, jsonify
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType

app = Flask(__name__)

spark = SparkSession.builder.appName("CourseAPI").getOrCreate()

model_1_path = "kafka-model/spark_kmeans_model_a"  
model_2_path = "kafka-model/spark_kmeans_model_b"  
model_3_path = "kafka-model/spark_kmeans_model_c"  
model_1 = KMeansModel.load(model_1_path)
model_2 = KMeansModel.load(model_2_path)
model_3 = KMeansModel.load(model_3_path)

# Model 1: Popularity and Engagement of Courses
schema_1 = StructType([
    StructField("num_subscribers", FloatType(), True),
    StructField("num_reviews", FloatType(), True),
    StructField("num_lectures", FloatType(), True),
    StructField("content_duration", FloatType(), True)
])
assembler_1 = VectorAssembler(
    inputCols=["num_subscribers", "num_reviews", "num_lectures", "content_duration"], 
    outputCol="features"
    )

# Model 2: Course Difficulty and Content 
schema_2 = StructType([
    StructField("num_subscribers", FloatType(), True),
    StructField("num_reviews", FloatType(), True),
    StructField("num_lectures", FloatType(), True),
    StructField("content_duration", FloatType(), True)
])
assembler_2 = VectorAssembler(
    inputCols=["num_subscribers", "num_reviews", "num_lectures", "content_duration"], 
    outputCol="features"
    )

# Model 3: Course price analysis
schema_3 = StructType([
    StructField("price", FloatType(), True),
    StructField("num_subscribers", FloatType(), True),
    StructField("num_reviews", FloatType(), True),
    StructField("content_duration", FloatType(), True)
])
assembler_3 = VectorAssembler(
    inputCols=["price", "num_subscribers", "num_reviews", "content_duration"],
    outputCol="features"
    )

# Endpoint 1: Popularity and Engagement of Courses
@app.route("/course_popularity", methods=["POST"])
def course_popularity():
    try:
        data = request.get_json()
        num_subscribers = data.get("num_subscribers")
        num_reviews = data.get("num_reviews")
        num_lectures = data.get("num_lectures")
        content_duration = data.get("content_duration")

        if None in [num_subscribers, num_reviews, num_lectures, content_duration]:
            return jsonify({"error": "Missing input data"}), 400

        input_data = [(float(num_subscribers), float(num_reviews), float(num_lectures), float(content_duration))]
        input_df = spark.createDataFrame(input_data, schema=schema_1)
        transformed_df = assembler_1.transform(input_df)

        predictions = model_1.transform(transformed_df)
        cluster = predictions.select("prediction").collect()[0]["prediction"]

        return jsonify({
            "model": "Popularity and Engagement of Courses",
            "input_data": data,
            "predicted_cluster": int(cluster)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint 2: Course Difficulty and Content
@app.route("/course_difficulty", methods=["POST"])
def course_difficulty():
    try:
        data = request.get_json()
        num_subscribers = data.get("num_subscribers")
        num_reviews = data.get("num_reviews")
        num_lectures = data.get("num_lectures")
        content_duration = data.get("content_duration")

        if None in [num_subscribers, num_reviews, num_lectures, content_duration]:
            return jsonify({"error": "Missing input data"}), 400

        input_data = [(float(num_subscribers), float(num_reviews), float(num_lectures), float(content_duration))]
        input_df = spark.createDataFrame(input_data, schema=schema_2)
        transformed_df = assembler_2.transform(input_df)

        predictions = model_3.transform(transformed_df)
        cluster = predictions.select("prediction").collect()[0]["prediction"]

        return jsonify({
            "model": "Course Difficulty and Content",
            "input_data": data,
            "predicted_cluster": int(cluster)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint 3: Course Price Analysis
@app.route("/course_price_analysis", methods=["POST"])
def course_price_analysis():
    try:
        data = request.get_json()
        price = data.get("price")
        num_subscribers = data.get("num_subscribers")
        num_reviews = data.get("num_reviews")
        content_duration = data.get("content_duration")

        if None in [price, num_subscribers, num_reviews, content_duration]:
            return jsonify({"error": "Missing input data"}), 400

        input_data = [(float(price), float(num_subscribers), float(num_reviews), float(content_duration))]
        input_df = spark.createDataFrame(input_data, schema=schema_3)
        transformed_df = assembler_3.transform(input_df)

        predictions = model_1.transform(transformed_df)
        cluster = predictions.select("prediction").collect()[0]["prediction"]

        return jsonify({
            "model": "Course Price Analysis",
            "input_data": data,
            "predicted_cluster": int(cluster)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)