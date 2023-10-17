import os
import django
from django.conf import settings
import os

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "t2_abckend.settings") 
# Replace 'YOUR_PROJECT_NAME' with the name of your Django project
django.setup()

from skynet.models import Orbit 
# Replace 'YOUR_APP_NAME' with the name of the app where your models are located

def insert_orbit_data():
    """Function to insert data into the Orbit model"""
    
    orbit = Orbit(
        JCAT='JCAT1234',  # Just a sample value. Replace with your desired value
        OpOrbitOQU='Sample Orbit',
        inclination=23.5,
        perigee=1000,
        apogee=2000,
        primary_planet='Earth'
    )
    
    orbit.save()
    print("Data inserted successfully!")

if __name__ == "__main__":
    insert_orbit_data()
