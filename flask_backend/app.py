import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        host="192.168.10.123",
        port="5432",
        user="postgres",
        password="skynet",
        dbname="skynet"
    )

@app.route('/api/satellites', methods=['GET'])
def get_satellites():
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM skynet_satellites')

        # Fetch all rows
        results = cursor.fetchall()

        # Get column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows to dictionaries using column names
        data = [dict(zip(column_names, row)) for row in results]

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
