"""
routines.py file

This file is where the states for the State Machine are defined. 

Overview: 
1. Import necessary libraries
2. Create routines for every state 

Note: This method is our reccomended best practice
"""

# Import logger from the runtime.py file to enable logging 
# Import Any from typing to allow "any" type hint
from runtime import logger
from typing import Any

# The MainRoutine handles switching to and from the Idle State.
# This is dependent on if the ProCaaSo Anywhere UI is triggered. 
def MainRoutine(**kwds: Any):
    sm = kwds['stateMachine']
    # Check if the start button on the ProCaaSo AnyWhere UI
    # is pressed to enter the Running State.
    try: 
        if  sm.get_instruments()['batch_cmd'].cmd.data.start == True:
            sm.transition_state(1) # Transition to the Running Routine
            sm.get_instruments()['batch_cmd'].state.data.state = 3 # Running State
            sm.get_instruments()['batch_cmd'].state.data.display = "Running" # UI Display String
            sm.get_instruments()['batch_cmd'].cmd.data.start = False

    # Check to see if the stop button on the ProCaaSo Anywhere UI is
    # triggered.
        elif sm.get_instruments()['batch_cmd'].cmd.data.abort == True:
            sm.transition_state(4) #Transition to the Abort Routine
    except Exception as e:
        logger.error(f"Error in Main Routine: {e}")

def on_enter_idle(**kwds: Any):
    sm = kwds['stateMachine']
    logger.info("Entering Idle State!")
    sm.get_instruments()['slider'].state.data.target_position = 0
    logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")


# The Idle Routine allows the hardware to remain Idle until the
# Run Button on the ProCaaso Anywhere UI is Triggered
def IdleRoutine(**kwds: Any): # We will give the Running State a "State ID" = 0
    sm = kwds['stateMachine']
    try:
        # Display the correct values to the UI 
        sm.get_instruments()['batch_cmd'].state.data.state = 0 # Idle State
        sm.get_instruments()['batch_cmd'].state.data.display = "Idle" # Display String to UI
        logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")
    except Exception as e: 
        logger.error(f"Error in the Idle State: {e}")


def on_enter_running(**kwds: Any):
    sm = kwds['stateMachine']
    logger.info("Entering Running State!")
    sm.get_instruments()['slider'].state.data.target_position = 20000
    logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")

# The Running Routine will move the slider 20,000 steps forward
# and transition to the Return Routine once completed. If the stop button is triggered
# on the ProCaaSo Anywhere UI, the State Machine will transition to the Abort Routine.
def RunningRoutine(**kwds: Any): # We will give the Running State a "State ID" = 1
    sm = kwds['stateMachine']
    try: 
        logger.debug("Moving Forward!")
        logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")
        sm.get_instruments()['batch_cmd'].state.data.state = 3
        sm.get_instruments()['batch_cmd'].state.data.display = "Running"
        sm.transition_state(2)
    except Exception as e: 
        logger.error(f"Error in the Running Routine: {e}")

def on_enter_return(**kwds: Any):
    sm = kwds['stateMachine']
    logger.info("Entering Return State!")
    sm.get_instruments()['slider'].state.data.target_position = -20000
    logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")

# The Return Routine will move the slider 20,000 steps backward and return to the Running Routine. 
# If the stop button is selected on the ProCaaSo UI. It will then transition to the Abort State
def ReturnRoutine(**kwds: Any): # We will give the Running State a "State ID" = 2
    sm = kwds['stateMachine']
    try: 
        logger.debug("Moving Backward!")
        logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")
        sm.get_instruments()['batch_cmd'].state.data.state = 3
        sm.get_instruments()['batch_cmd'].state.data.display = "Running"
        sm.transition_state(1)
    except Exception as e: 
        logger.error(f"Error in the Running Routine: {e}")

def on_enter_abort(**kwds: Any):
    sm = kwds['stateMachine']
    logger.info("Entering Abort State!")
    sm.get_instruments()['slider'].state.data.target_position = 0
    logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")
    # Transition back to the Idle Routine
    sm.transition_state(0)

# The Abort Routine will halt the slider from moving, and transition to the Idle State
def AbortRoutine(**kwds: Any):
    sm = kwds['stateMachine']
    try:

        # Display the correct values to the UI 
        sm.get_instruments()['batch_cmd'].state.data.state = 4 # Abort State
        sm.get_instruments()['batch_cmd'].state.data.display = "Aborting" # UI Display String
        # Set the stepper motor's target position to 0 so that it does not move
        logger.debug(f"Stepper motor position = {sm.get_instruments()['slider'].state.data.target_position}")

    except Exception as e:
        logger.error(f"Error in Abort Routine: {e}")

