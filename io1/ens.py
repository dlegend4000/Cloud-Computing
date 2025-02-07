"""
ens.py file -- (IO TASK)

This is the USER ENTRY POINT file. This file begins the execution of the user code and
allows for data communication to and from the Event Bus.

Overview: 
1. Import neccessary libraries
2. Define a dictionary to store IO Map data for the hub component
3. Retrieve IO Map data from Event But and store in the dictionary
4. Define a startup expression to post the start up event
5. Define logic to handle hardware connection
6. Start the application
"""

from runtime import io, logger
from user_code.models import *
from user_code.cip_objects import PhidgetSBC4
from user_code.sensor_io_logic import sensor_user_logic
from user_code.stepper_io_logic import slider_user_logic

# Define a startup expression to post the start up event using post_start_up_event()
@io.startup_expression
def startup():
    io.client.get_runtime_event()

    # Define a dictionary to store IO Mapping data for the hub component
    mapping_dict = {"sensor": [], "slider": []}

    test = io.client.get_system_io_maps_definition()
    # Debug to verify 

    # Fetch I/O mapping data for the components using the 'app' client and store it in the dictionary
    # using get_io_maps()
    mapping_dict["sensor"] = io.client.get_io_maps(component_name="Distance Sensor")
    mapping_dict["slider"] = io.client.get_io_maps(component_name="Slider")
    logger.debug(f"This is verify that the IO Map data was retrieved from the Event Bus: \n {mapping_dict}")

    # Define a startup expression to post the start up event using post_start_up_event()
    """
    Utilizing for loops allows for iteratation over lists of I/O mapping data for each component type, the code dynamically
    generates expressions and logic tailored to each component, thus facilitating the synchronization of multiple 
    components with the Python code and I/O map. However, there is only one hardware component that we are 
    tying the user code to the IO Map to in this example.

    """
    # Logic responsible for handling hub connection
    for x, obj in enumerate(mapping_dict["sensor"]):
        # Define an expression for hub logic and order it based on the enumeration
        # Parameters: 'comm_object' for communication and 'test' for the current object
        @io.expression(order=x, comm_object=PhidgetSBC4(uid=obj['Maps'][0]['value'], host=obj['Maps'][0]['value']))
        def add_instance(comm_object):
            # Return an instance of 'hub_logic' from phidget_io_logic.py with the provided parameters
            return sensor_user_logic(comm_object=comm_object, client=io.client)
        # Logic responsible for handling hub connection
    for x, obj in enumerate(mapping_dict["slider"]):
        # Define an expression for hub logic and order it based on the enumeration
        # Parameters: 'comm_object' for communication and 'test' for the current object
        @io.expression(order=x, comm_object=PhidgetSBC4(uid=obj['Maps'][0]['value'], host=obj['Maps'][0]['value']))
        def add_instance(comm_object):
            # Return an instance of 'hub_logic' from phidget_io_logic.py with the provided parameters
            return slider_user_logic(comm_object=comm_object, client=io.client)

# Start the appication.
io.start()