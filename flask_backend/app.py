from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Satellite, SatelliteEditRecord, RecordTable
import os
from sqlalchemy import func
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/satellites', methods=['GET'])
def get_satellites():
    try:
        # Query the skynet_satellites table
        results = Satellite.query.filter(Satellite.data_status != 2).all()

        # Serialize the results into a list of dictionaries
        data = [row.to_dict() for row in results] # Make sure this method exists in your model

        return jsonify(data)
    except Exception as e:
        # Log the exception for debugging purposes
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/removed', methods=['GET'])
def get_removed_satellites():
    try:
        # Query the skynet_satellites table for removed satellites (data_status = 1)
        results = Satellite.query.filter(Satellite.data_status == 1).all()

        # Serialize the results into a list of dictionaries
        data = [row.to_dict() for row in results] # Assuming you have a to_dict() method in your model

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    satellite_names = [item['satellite_name'] for item in data['updatedItems']]
    name = data.get('name', 'Unknown')
    current_date = datetime.now()

    try:
        for satellite_name in satellite_names:
            # Update the SkynetSatellite table
            satellite = Satellite.query.filter_by(satellite_name=satellite_name).first()
            if satellite:
                satellite.data_status = 2
                db.session.add(satellite)

                # Debug print
                print(f"Updating satellite: {satellite}")

                # Insert a record into the RecordTable
                new_record = RecordTable(name=name, date=current_date, satellite_name=satellite_name)
                db.session.add(new_record)

                # Debug print
                print(f"Adding record for: {satellite}")

        db.session.commit()
        return jsonify({"message": "Status updated and record added successfully"}), 200
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
            RecordTable.satellite_name
        ).all()

        # Serialize the results into a list of dictionaries
        data = [{'name': r.name, 'date': r.date, 'satellite_name': r.satellite_name} for r in results]

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/details', methods=['GET'])
def get_jcat_details():
    try:
        satellite_name = request.args.get('satellite_name')
        satellites = Satellite.query.filter_by(satellite_name=satellite_name).all()
        satellites_details = []
        satellites_details.extend([satellite.to_dict() for satellite in satellites])
        return jsonify(satellites_details)
    except Exception as e:
        app.logger.error('Error in get_jcat_details: ' + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/edit-data', methods=['POST'])
def edit_data():
    try:
        data = request.json
        edit_records = data['edit_records']
        edited_by = data['name']

        print("Received edit records:", edit_records)  # Debug print

        for record in edit_records:
            print(f"Processing record for satellite_name: {record['satellite_name']}")  # Debug print

            # Insert into satellite_edit_records
            new_edit_record = SatelliteEditRecord(
                satellite_name=record['satellite_name'],
                column_name=record['column'],
                old_value=record['oldValue'],
                new_value=record['newValue'],
                edited_by=edited_by
            )
            db.session.add(new_edit_record)

            # Update skynet_satellites
            update_result = Satellite.query.filter_by(satellite_name=record['satellite_name']).update({record['column']: record['newValue']})
            print(f"Update result for satellite_name {record['satellite_name']}: {update_result}")  # Debug print

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)
