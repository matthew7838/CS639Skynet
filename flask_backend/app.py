from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Satellite_New, Satellite_Master, Master_Edit_Record, RecordTable, User, SatelliteRemovalRecord, Satellite_Removed, ApproveDenyTable, ScrapeRecord, New_Edit_Record
from functools import wraps
import os
import traceback
import jwt
from sqlalchemy import func
from datetime import datetime, timedelta
import subprocess
from sqlalchemy import not_


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
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 100, type=int)
        offset = (page - 1) * limit

        # Search query parameter
        search_query = request.args.get('search', '', type=str)

        # Query with optional filtering
        query = Satellite_New.query.filter(not_(Satellite_New.data_status.in_([3, 4, 5])))
        if search_query:
            query = query.filter(func.lower(Satellite_New.cospar).like(f'%{search_query.lower()}%'))  # Example for filtering by name

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
        query = Satellite_Master.query.filter(not_(Satellite_Master.data_status.in_([3, 4])))
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

#NEW_LAUNCHES
@app.route('/api/satellites_removed', methods=['GET'])
def get_satellites_removed():
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 100, type=int)
        offset = (page - 1) * limit

        # Search query parameter
        search_query = request.args.get('search', '', type=str)

        query = Satellite_Removed.query
        if search_query:
            query = query.filter(func.lower(Satellite_Removed.cospar).like(f'%{search_query.lower()}%'))  # Example for filtering by name

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
            # Fetch the satellite to be updated
            satellite = Satellite_Master.query.filter_by(cospar=cospar).first()
            if satellite:
                # Update data_status to 4
                satellite.data_status = 4
                db.session.add(satellite)

                # Fetch the removal reason
                removal_record = SatelliteRemovalRecord.query.filter_by(cospar=cospar).first()
                removal_reason = removal_record.reason if removal_record else "Unknown"

                # Add to Satellite_Removed
                removed_satellite = Satellite_Removed(
                    **satellite.to_dict(),  # assuming to_dict() method converts the satellite object to a dictionary
                    removal_source='ucs_master',
                    removal_reason=removal_reason
                )
                db.session.add(removed_satellite)

                # Insert a record into the RecordTable
                new_record = RecordTable(name=name, date=current_date, cospar=cospar)
                db.session.add(new_record)

                # Debug print
                print(f"Updated satellite {cospar} status to 4 and added to Satellite_Removed")

        db.session.commit()
        return jsonify({"message": "Satellite status updated, added to Satellite_Removed, and record added successfully"}), 200
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
def get_removed_master_sat_details():
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
def master_edit_data():
    try:
        data = request.json
        edit_records = data['edit_records']
        edited_by = data['name']

        print("Received edit records:", edit_records)  # Debug print

        for record in edit_records:
            print(f"Processing record for cospar: {record['cospar']}")  # Debug print

            # Insert into satellite_edit_records
            new_edit_record = Master_Edit_Record(
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
def get_master_edit_records():
    try:
        
        # Log at the start
        app.logger.info('get_edit_records function called')

        # Query all records in the satellite_edit_records table
        records = Master_Edit_Record.query.all()

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
    
@app.route('/api/ucs_new/edit-data', methods=['POST'])
def new_edit_data():
    try:
        data = request.json
        edit_records = data['edit_records']
        edited_by = data['name']

        print("Received edit records:", edit_records)  # Debug print

        for record in edit_records:
            print(f"Processing record for cospar: {record['cospar']}")  # Debug print

            # Insert into satellite_edit_records
            new_edit_record = New_Edit_Record(
                cospar=record['cospar'],
                column_name=record['column'],
                old_value=record['oldValue'],
                new_value=record['newValue'],
                edited_by=edited_by
            )
            db.session.add(new_edit_record)

            # Update skynet_satellites
            update_result = Satellite_New.query.filter_by(cospar=record['cospar']).update(
                {record['column']: record['newValue']})
            print(f"Update result for satellite_name {record['cospar']}: {update_result}")  # Debug print

        db.session.commit()
        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")  # More detailed error message
        return jsonify({'error': str(e)}), 500

@app.route('/api/ucs_new/get-edit-records', methods=['GET'])
def get_new_edit_records():
    try:
        
        # Log at the start
        app.logger.info('get_edit_records function called')

        # Query all records in the satellite_edit_records table
        records = New_Edit_Record.query.all()

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

@app.route('/api/ucs_new/new_satellites_approve', methods=['POST'])
def confirm_approval():
    print('Function confirm_approval called')

    data = request.get_json()
    row_data = data.get('row')  # This will be a dictionary containing the row data
    print(row_data)
    
    name = data.get('name', 'Unknown')
    reason = data.get('reason')
    print(f'Received name: {name}')

    current_date = datetime.now()
    print(f'Current date: {current_date}')

    try:
        # Remove 'editing' key from row_data if it exists
        row_data.pop('editing', None)

                # Update the data_status in Satellites_New
        satellite_new = Satellite_New.query.filter_by(cospar=row_data.get('cospar')).first()
        if satellite_new:
            satellite_new.data_status = 5  # Update to the desired status
            db.session.add(satellite_new)
            print(f"Updated data_status in Satellites_New for {row_data.get('cospar')}")

        # Create a new instance for Satellite_Master using the row data
        new_satellite = Satellite_Master(**row_data)
        db.session.add(new_satellite)
        print(f"New satellite added to Satellite_Master: {row_data}")

        # Insert a record into ApproveDenyTable
        approval_record = ApproveDenyTable(name=name, date=current_date, cospar=row_data.get('cospar'), action="approve", reason = reason)
        db.session.add(approval_record)
        print(f"Added record to ApproveDenyTable for satellite {row_data.get('cospar')}")

        db.session.commit()
        return jsonify({"message": "New satellite added to Satellite_Master and approval record added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Exception occurred: {e}')  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/api/ucs_new/new_satellites_deny', methods=['POST'])
def deny_approval():
    print('Function deny_approval called')

    data = request.get_json()
    row_data = data.get('row')  # This will be a dictionary containing the row data
    print(row_data)
    
    name = data.get('name', 'Unknown')
    reason = data.get('reason')
    print(f'Received name: {name}')

    current_date = datetime.now()
    print(f'Current date: {current_date}')

    cospar = row_data.get('cospar')

    try:
        # Update the data_status in Satellite_New
        satellite_new = Satellite_New.query.filter_by(cospar=cospar).first()
        if satellite_new:
            satellite_new.data_status = 4  # Assuming 4 indicates a denied status
            db.session.add(satellite_new)
            print(f"Updated data_status in Satellite_New for {cospar} to 4 (denied)")

            # Add to Satellite_Removed
            removed_satellite = Satellite_Removed(
                **satellite_new.to_dict(),  # assuming to_dict() method converts the satellite object to a dictionary
                removal_source='ucs_new',
                removal_reason=reason
            )
            db.session.add(removed_satellite)
            # Insert a record into ApproveDenyTable
            denial_record = ApproveDenyTable(name=name, date=current_date, cospar=cospar, action="deny", reason = reason)
            db.session.add(denial_record)
            print(f"Added denial record to ApproveDenyTable for satellite {cospar}")

        db.session.commit()
        return jsonify({"message": "Satellite denial confirmed and records added successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Exception occurred: {e}')  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/api/new_history', methods=['GET'])
def get_new_history():
    try:
        # Perform the query to get all records from ApproveDenyTable
        results = ApproveDenyTable.query.all()

        # Serialize the results into a list of dictionaries
        data = [{'name': r.name, 'date': r.date, 'cospar': r.cospar, 'action': r.action, 'reason':r.reason} for r in results]

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/ucs_new/history/details', methods=['GET'])
def get_new_removed_sat_details():
    try:
        cospar = request.args.get('cospar')

        # Perform a join with the SatelliteRemovalRecord table
        results = db.session.query(
            Satellite_New, 
            ApproveDenyTable.reason
        ).outerjoin(
            ApproveDenyTable, 
            Satellite_New.cospar == ApproveDenyTable.cospar
        ).filter(Satellite_New.cospar == cospar).all()

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




if __name__ == "__main__":
    app.run(debug=True, port=8000)
