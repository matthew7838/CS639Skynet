from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Satellite_New, Satellite_Master, SatelliteEditRecord, RecordTable, User, SatelliteRemovalRecord, Satellite_Removed
from functools import wraps
import os
import traceback
import jwt
from sqlalchemy import func
from datetime import datetime, timedelta
import subprocess


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Debugging: Check values
        print("Debug - Username: ", user.username)
        print("Debug - Login Date: ", datetime.now().date().isoformat())
        print("Debug - Secret Key: ", app.config['SECRET_KEY'])

        # Generate token
        token = jwt.encode({
            'username': user.username,
            'login_date': datetime.now().date().isoformat(),
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        # Debugging: Check token
        print("Debug - Generated Token: ", token)

        return jsonify({'token': token, 'username': user.username}), 200

    return jsonify({'error': 'Invalid username or password'}), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        # Debugging: Check received token
        print("Debug - Received Token: ", token)

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Debugging: Check decoded data
            print("Debug - Decoded Data: ", data)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated


@app.route('/some-protected-route')
@token_required
def protected_route():
    return 'This is a protected route.'


#NEW_LAUNCHES
@app.route('/api/satellites_new', methods=['GET'])
def get_satellites_new():
    try:
        # Query the skynet_satellites table
        results = Satellite_New.query.filter().all()

        # Serialize the results into a list of dictionaries
        data = [row.to_dict() for row in results]  # Make sure this method exists in your model

        return jsonify(data)
    except Exception as e:
        # Log the exception for debugging purposes
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    
#master_dataset
@app.route('/api/satellites_master', methods=['GET'])
def get_satellites_master():
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 100, type=int)
        offset = (page - 1) * limit

        # Search query parameter
        search_query = request.args.get('search', '', type=str)

        # Query with optional filtering
        query = Satellite_Master.query.filter(Satellite_Master.data_status != 3)
        if search_query:
            query = query.filter(func.lower(Satellite_Master.cospar).like(f'%{search_query.lower()}%'))  # Example for filtering by name

        # Get total count after filtering
        total_count = query.count()

        # Apply pagination
        results = query.offset(offset).limit(limit).all()

        # Convert data to dict
        data = [row.to_dict() for row in results]

        return jsonify({
            'data': data,
            'total_count': total_count
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500



@app.route('/api/removed', methods=['GET'])
def get_removed_satellites():
    try:
        # Query the skynet_satellites table for removed satellites (data_status = 1)
        results = db.session.query(
            Satellite_Master, 
            SatelliteRemovalRecord.reason
        ).join(
            SatelliteRemovalRecord, 
            Satellite_Master.cospar == SatelliteRemovalRecord.cospar
        ).filter(Satellite_Master.data_status == 3).all()

        # Serialize the results into a list of dictionaries
        data = [
            {
                **row.Satellite_Master.to_dict(), 
                "removal_reason": row.reason
            } for row in results
        ]

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    cospar_list = data['cospar_list']
    print(cospar_list)
    name = data.get('name', 'Unknown')
    current_date = datetime.now()

    try:
        for cospar in cospar_list:
            # Fetch the satellite to be removed
            satellite = Satellite_Master.query.filter_by(cospar=cospar).first()
            if satellite:
                # Fetch the removal reason
                removal_record = SatelliteRemovalRecord.query.filter_by(cospar=cospar).first()
                removal_reason = removal_record.reason if removal_record else "Unknown"

                # Add to Satellite_Removed
                removed_satellite = Satellite_Removed(
                    **satellite.to_dict(),  # assuming to_dict() method converts the satellite object to a dictionary
                    remove_source='ucs_master',
                    remove_reason=removal_reason
                )
                db.session.add(removed_satellite)

                # Delete from Satellite_Master
                db.session.delete(satellite)

                # Insert a record into the RecordTable
                new_record = RecordTable(name=name, date=current_date, cospar=cospar)
                db.session.add(new_record)

                # Debug print
                print(f"Removed satellite {cospar} and added to Satellite_Removed")

        db.session.commit()
        return jsonify({"message": "Satellite removed, status updated, and record added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")  # Debug print
        return jsonify({"error": str(e)}), 500



@app.route('/api/history', methods=['GET'])
def get_history_records():
    try:
        # Perform the query to get all records
        results = db.session.query(
            RecordTable.name, 
            RecordTable.date, 
            RecordTable.cospar
        ).all()

        # Serialize the results into a list of dictionaries
        data = [{'name': r.name, 'date': r.date, 'cospar': r.cospar} for r in results]

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/history/details', methods=['GET'])
def get_cospar_details():
    try:
        cospar = request.args.get('cospar')

        # Perform a join with the SatelliteRemovalRecord table
        results = db.session.query(
            Satellite_Master, 
            SatelliteRemovalRecord.reason
        ).outerjoin(
            SatelliteRemovalRecord, 
            Satellite_Master.cospar == SatelliteRemovalRecord.cospar
        ).filter(Satellite_Master.cospar == cospar).all()

        # Serialize the results
        satellites_details = []
        for satellite, reason in results:
            satellite_dict = satellite.to_dict()
            satellite_dict['removal_reason'] = reason
            satellites_details.append(satellite_dict)

        return jsonify(satellites_details)
    except Exception as e:
        app.logger.error('Error in get_cospar_details: ' + str(e))
        return jsonify({"error": str(e)}), 500



@app.route('/api/edit-data', methods=['POST'])
def edit_data():
    try:
        data = request.json
        edit_records = data['edit_records']
        edited_by = data['name']

        print("Received edit records:", edit_records)  # Debug print

        for record in edit_records:
            print(f"Processing record for cospar: {record['cospar']}")  # Debug print

            # Insert into satellite_edit_records
            new_edit_record = SatelliteEditRecord(
                cospar=record['cospar'],
                column_name=record['column'],
                old_value=record['oldValue'],
                new_value=record['newValue'],
                edited_by=edited_by
            )
            db.session.add(new_edit_record)

            # Update skynet_satellites
            update_result = Satellite_Master.query.filter_by(cospar=record['cospar']).update(
                {record['column']: record['newValue']})
            print(f"Update result for satellite_name {record['cospar']}: {update_result}")  # Debug print

        db.session.commit()
        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")  # More detailed error message
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-edit-records', methods=['GET'])
def get_edit_records():
    try:
        
        # Log at the start
        app.logger.info('get_edit_records function called')

        # Query all records in the satellite_edit_records table
        records = SatelliteEditRecord.query.all()

        # Log query execution
        app.logger.info(f'Query executed, retrieved {len(records)} records')

        # Serialize the records into a list of dictionaries
        data = [record.to_dict() for record in records]

        # Log before returning
        app.logger.info('Successfully serialized the records')

        return jsonify(data), 200
    except Exception as e:
        # Log the full exception
        app.logger.error('Error in get_edit_records: ' + str(e))
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/remove-sat', methods=['POST'])
def remove_sat():
    data = request.get_json()
    cospar_id = data.get('cospar')
    reason = data.get('reason')

    try:
        # Find the satellite using the cospar ID
        satellite = Satellite_Master.query.filter_by(cospar=cospar_id).first()
        if not satellite:
            return jsonify({'error': 'Satellite not found'}), 404

        # Update the satellite status to indicate it has been removed
        satellite.data_status = 3
        db.session.add(satellite)

        # Create a new removal record
        new_removal_record = SatelliteRemovalRecord(cospar=cospar_id, reason=reason)
        db.session.add(new_removal_record)

        db.session.commit()
        return jsonify({'message': 'Satellite removed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/run-scraper', methods=['POST'])
def run_scraper():
    try:
        data = request.get_json()
        username = data['name']
        # Existing code
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Adjusting to get the desired path
        desired_path = os.path.dirname(os.path.dirname(base_dir))

        script_path = os.path.join(desired_path, 'CS639Skynet', 'skynet_scrapy', 'myspider', 'skynet.py')
        print(script_path)

        # Run the command
        subprocess.run(['python', script_path], check=True)
        scraper_completion(username)
        return jsonify({"message": "Scraper started successfully"}), 200
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the scraper: {e}")
        return jsonify({'error': 'Failed to run scraper'}), 500
    except Exception as e:
        print(f"General Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/scraper-completion', methods=['POST'])
def scraper_completion(username):
    try:

        # Create a new ScrapeRecord instance
        new_record = ScrapeRecord(username=username)
        db.session.add(new_record)
        db.session.commit()

        return jsonify({'message': 'New scrape record added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/scrape-records', methods=['GET'])
def get_scrape_records():
    try:
        print("Fetching scrape records...")
        records = ScrapeRecord.query.all()

        print(f"Records fetched: {records}")

        # Convert the records to a list of dictionaries
        data = [record.to_dict() for record in records]

        print(f"Data to return: {data}")

        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching scrape records: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=8000)
