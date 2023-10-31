from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)

# Define database connection parameters
HOSTNAME = 'localhost'
PORT = 5432
USERNAME = 'skynet-username'
PASSWORD = 'skynet-password'
DATABASE = 'skynet_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"

db = SQLAlchemy(app)

# Test database connection
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())

@app.route('/')
def hello_world():
    return 'Hello World!'
