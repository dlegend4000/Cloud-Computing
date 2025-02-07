"""
phidget_io_logic.py

This file defines the comunnication IO Logic for the Phidget Hub. This is an API based implementation, 
so we send GET Requests and POST Requests to the Phidget Hub server to read and write data from 
the Event Bus. 

Overview:
1. Import necessary libraries
2. Define a function that includes IO Logic
    a. Retrieve attribute data from the Event Bus
    b. Logic to send GET request to Phidget Server
    c. Logic to send POST request to Phidget Server
    d. Write updated data from Phidget Server to the Event Bus
"""
# Import from procaaso_client to read/write data from the Event Bus,
# import PhidgetSBC4 class from cip_objects.py to retrieve unique identifier sfrom IO Map,
# import Hub models from models.py, import logger to enable logging, import requests to
# enable POST/GET requests to Phidget Server, import json to convert data from the Event 
# Bus to JSON 
from procaaso_client.synchronous.client import SyncHarnessClient
from user_code.cip_objects import PhidgetSBC4
from user_code.models import SliderState, SliderUDT
from runtime import logger
import requests
import json

# Define a function to handle IO Logic - Parameters: comm_object -- retrieves data from IO Map
# client -- enables access to the Event Bus
def slider_user_logic(
    comm_object: PhidgetSBC4, client: SyncHarnessClient
) -> None:

    # Retrieve Hub state attribute data using get_attribute_state() -- Similar to App Task ens 
    try:
        state: SliderState = client.get_attribute_state(
            value_model= SliderState, **SliderUDT().state.fqn_dict()
        )
        logger.debug(f"Slider: {comm_object}")
    except Exception as e:
        logger.error(f"Slider: Error in assigning Hub state: {e}")

    # Send stepper position value from Event Bus to Phidget server.
    try:
        url = f"http://{comm_object.uniqueId}:8000/hub"
        stepper_data = {
            "target_position": state.target_position,
        }

        jsonified_stepper_data = json.dumps(stepper_data)
        logger.debug(f"JSONified stepper data: {jsonified_stepper_data}")

        # Create headers for POST request
        stepper_headers = {"Content-Type": "application/json"}

        # Send state to the Phidget
        stepper_response = requests.post(url, data=jsonified_stepper_data, headers=stepper_headers)
        logger.debug(f"Response from PhidgetSBC4 server: {stepper_response}")

        if stepper_response.status_code == 200:
            # Successful POST request
            logger.debug("POST request was successful.")
        else:
            logger.debug(f"POST request failed with status code {stepper_response.status_code}")

    except Exception as e:
        logger.error(f"Error in POST request to Phidget Server {e}")

    #Post updated Hub state attribute data using post_attribute_state()
    try:
        
        client.post_attribute_state(value=state, **SliderUDT().state.fqn_dict())
    except Exception as e:
        logger.error(f"Error in posting hub attribute state: {e}")