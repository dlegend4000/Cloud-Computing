"""
ens.py file -- (APP TASK)

This is the USER ENTRY POINT file. This file begins the execution of the user code and
allows for data communication to and from the Event Bus.

Overview: 
1. Import necessary libraries
2. Initialize a state machine object to be used globally
3. Define a start up expression to clear the existing cache, retrieve the runtime event,
   and initialize the state machine 
4. Define expressions to: 
    a. Read data from the Event Bus 
    b. Use data from the Event Bus to execute the user written control logic
    c. Write data to the Event Bus
7. Start the application

"""
# Import necessities -- Import  the ProCaaSo State Machine library 
# import all the state machine states from routines.py,
# import model objects from global_tags.py, and
# import instance of ProCaaSo Programmers Framework API from runtime.py
from procaaso_state_machine.procaaso_state_machine import StateMachine, State
from user_code.routines import *
from user_code.global_tags import *
from runtime import app, logger 

# Create the StateMachine object outside the function calls
# so it is available throughout all the expressions

sm = StateMachine()

# Define a startup expression to clear existing cache, get runtime events 
# and initialize the State Machineapp.client.get_runtime_event()a

@app.startup_expression
def startup():
    # This clears the existing cache
    app.client.post_startup_event()
    # This retrieves the runtime event
    app.client.get_runtime_event()
    # Initialize the State Machine
    
    # Initialize each State object and assign each state a "State ID"
        # Notice that the variable naming convention is different than
        # the functions defined in the routines.py fle. 
        # This is because we are making new objects
        # that use the functions we created in our routine.py file
    try: 
        idleState = State(0, onEnterEnabled=True, onExitEnabled=False)
        runningState = State(1, onEnterEnabled=True, onExitEnabled=False)
        returnState = State(2, onEnterEnabled=True, onExitEnabled=False)
        abortState = State(4, onEnterEnabled=True, onExitEnabled=False)
    except Exception as e:
        logger.error(f"Error creating one or more of the states: {e}")

    # Setting onEnter functions
    try:
        idleState.set_on_enter_function(on_enter_idle)
        runningState.set_on_enter_function(on_enter_running)
        returnState.set_on_enter_function(on_enter_return)
        abortState.set_on_enter_function(on_enter_abort)
    except Exception as e:
        logger.error(f"Error in setting onEnter functions{e}")

    # Add all the possible transitions for each state using the
    # set_transition(), and set all of the routines associated with the states
    # using the set_routine()

    try: 
        idleState.set_transition(1)
        idleState.set_transition(4)
        idleState.set_routine("routine", IdleRoutine)
        idleState.set_routine("main_routine", MainRoutine)
        # Notice you may add multiple routines to a state
    except Exception as e:
        logger.error(f"Error defining the Idle State")

    try: 
        runningState.set_transition(2)
        runningState.set_transition(4)
        runningState.set_routine("routine", RunningRoutine)
        runningState.set_routine("main_routine", MainRoutine)
    except Exception as e:
        logger.error(f"Error defining the Running State")

    try: 
        abortState.set_transition(0)
        abortState.set_routine("routine", AbortRoutine)
        abortState.set_routine("main_routine",MainRoutine)
    except Exception as e:
        logger.error(f"Error defining the Abort State")
    
    try:
        returnState.set_transition(1)
        returnState.set_transition(4)
        returnState.set_routine("routine", ReturnRoutine)
        returnState.set_routine("main_routine", MainRoutine)
    except Exception as e: 
        logger.error(f"Error defining the Return State")
    
    # Add all the defined states to the state machine using the add_state() function
    try: 
        sm.add_state(idleState)
        sm.add_state(runningState)
        sm.add_state(returnState)
        sm.add_state(abortState)
    except Exception as e:
        logger.error(f"Error adding one or more state to the state machine: {e}")

    # Add the instruments of the system to the state machine for global access using add_instrument(), 
    # create a dictionary to hold the data structure defined the global_tags.py file.
    ### You will need to add the env sensor instance HERE ###
    try:
        sm.add_instrument({"batch_cmd": batch_cmd, "sensor": sensor, "slider": slider})
    except Exception as e:
        logger.error(f"Error adding instruments to the state machine{e}")

    # Start the state machine and assign the starting state
    # based on it's State ID
    try:
        sm.start_state_machine(0) # We will start our state machine in the Idle state
    except Exception as e:
        logger.error(f"Error starting the state machine: {e}")


"""
Create expressions to read data from the Event Bus by using get_attribute_state()
Each @app.expression takes the parameter "order" to specify order priority. Expressions 
with lower numerical values for the "order" parameter will be executed first, thus 
taking priority over those with higher values. This approach ensures that expressions 
are executed in ascending numerical order based on their priority level.

"""

# Define an expression to read the batch state and cmd attribute data
@app.expression(order=0)
def batchDataRead():
    # Access our instrument data using the state machine with get_instruments()
    # Retrieve batch_cmd state attribute data
    try:
        sm.get_instruments()['batch_cmd'].state.data = app.client.get_attribute_state(
            value_model=sm.get_instruments()['batch_cmd'].state.data_type(), **sm.get_instruments()['batch_cmd'].state.fqn_dict()
        )
    except Exception as e:
        logger.error(f"Error accessing batch_cmd state instruments via State Machine: {e}")

    # Retrieve batch_cmd cmd attribute data
    try:
        sm.get_instruments()['batch_cmd'].cmd.data = app.client.get_attribute_state(
            value_model=sm.get_instruments()['batch_cmd'].cmd.data_type(), **sm.get_instruments()['batch_cmd'].cmd.fqn_dict()
        )
    except Exception as e:
        logger.error(f"Error in accessing batch_cmd cmd instruments: {e}")
    
    # Example of how to utilize the ProCaaSo Log Library to provide debug statements
    logger.debug("--------------------------------------")
    logger.debug(f"Batch state values after read: {sm.get_instruments()['batch_cmd'].state.data}")
    logger.debug(f"Batch cmd values after read: {sm.get_instruments()['batch_cmd'].cmd.data}")

# Define an expression to read sensor data. This is similar to access the batch_cmd data 
@app.expression(order=1)
def sensorDataRead():
    # Retrieve sensor state attribute data
    try:
        sm.get_instruments()['sensor'].state.data = app.client.get_attribute_state(
            value_model=sm.get_instruments()['sensor'].state.data_type(), **sm.get_instruments()['sensor'].state.fqn_dict()
        )
        logger.debug(f"Distance Sensor Reading: {sm.get_instruments()['sensor'].state.data.current_distance}")

    except Exception as e:
        logger.error(f"Failed to assign Sensor data: {e}")

### You will need Define an expression to read the Environmental Sensor Data ###




################################################################################
# Define the main expression that enables the State Machine (Control Logic) to run
@app.expression(order=3)
def main():
    # Run all the routines defined in the state machine initialization
    try:
        app.execution_delay = 0.5 # Seconds
        sm.run_routine("routine", log=logger)
        sm.run_routine("main_routine", log=logger)

    except Exception as e:
        logger.error(f"Error in Main Expression: {e}")

# Write updated data from State Machine to the Event Bus using post_attribute_state()

# Define an expression to write slider data 
@app.expression(order=4)
def sliderDataWrite():
    try:
        app.client.post_attribute_state(value=sm.get_instruments()['slider'].state.data, **sm.get_instruments()['slider'].state.fqn_dict())
    except Exception as e:
        logger.error(f"Error in writing slider data: {e}")

# Define an expression to write batch data.
@app.expression(order=5)
def batchDataWrite():
    try:
       app.client.post_attribute_state(value=sm.get_instruments()['batch_cmd'].state.data, **sm.get_instruments()['batch_cmd'].state.fqn_dict())
    except Exception as e:
        logger.error(f"Error in writing batch state data: {e}")
    try:
        app.client.post_attribute_state(value=sm.get_instruments()['batch_cmd'].cmd.data, **sm.get_instruments()['batch_cmd'].cmd.fqn_dict())
    except Exception as e:
        logger.error(f"Error in writing batch cmd data: {e}")

# Define an expression to write distance sensor data to UI.
@app.expression(order=6)
def sensorDataWrite():
    try:
        app.client.post_attribute_state(value=sm.get_instruments()['sensor'].state.data, **sm.get_instruments()['sensor'].state.fqn_dict())
    except Exception as e:
        logger.error(f"Error in writing sensor data: {e}")

### You will need to define an expression to write Environmental sensor data to Event Bus ###





#############################################################################################

# Start the application.
app.start()






































