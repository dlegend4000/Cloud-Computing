"""
models.py file

This file defines the Data Models that are associated with the 
StateSchemas from our system template and allows for attribute 
data communication (read/write) to and from the ProCaaSo 
Event Bus. This file will be EXACTLY the same in both the App and IO Tasks.

Overview: 
1. Import necessary libraries
2. Define a type variable for the state variable
3. Define the FullyQualifiedName class to enforce data type to match 
   the StateSchemas on the Event Bus
4. Define the Combined Model that combines the FullyQualifiedName and data of a model
5. Define a State Model class for every component in the System Definition
6. Create a Combined Models for every component 

Note: This method is our reccomended best practice to handle data communcation between
the Event Bus and User Code. 
"""

# Import pydantic -- Allows us to enforce data types
# Import typing -- Set up foundation for type hinting
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# Define a type variable for the state model
StateModelType = TypeVar("StateModelType", bound=BaseModel)

# Define a FullyQualifiedName model to represent a qualified attribute name from the Event Bus.
class FullyQualifiedName(BaseModel):
    system_name: Optional[str]
    component_name: Optional[str]
    connector_name: Optional[str]
    instrument_name: Optional[str]
    attribute_name: str

# Define a CombinedModel that combines FullyQualifiedName and data of a specified type.
class CombinedModel(Generic[StateModelType], BaseModel):
    fqn: FullyQualifiedName
    data: StateModelType

    def fqn_dict(self):
        return self.fqn.dict()

    def data_dict(self):
        return self.data.dict()

    def data_type(self):
        return type(self.data)

# Define Sensor Model for Sensor Communication and the UI   
class SensorState(BaseModel):
    home_distance: float = 0.0 # Target distance for "Home State" -- Needed for PID implementation
    target_distance: float = 0.0 # Target distance for "Running State" -- Needed for PID implementation
    current_distance: float = 0.0 # Current State that will be displayed to UI

# Define a SensorUDT model that combines FullyQualifiedName and Sensor data
class SensorUDT(BaseModel):
    state: CombinedModel[SensorState] = CombinedModel[SensorState](
        fqn=FullyQualifiedName(
            component_name="Distance Sensor",
            instrument_name="sensor",
            attribute_name="state",
        ),
        data=SensorState(),
    )

# Define Sensor Model for Slider Communication and UI Values
class SliderState(BaseModel):
    # Current states that will be displayed to UI
    target_position: int = 0

# Define a SliderUDT model that combines FullyQualifiedName and Slider data
class SliderUDT(BaseModel):
    state: CombinedModel[SliderState] = CombinedModel[SliderState](
        fqn=FullyQualifiedName(
            component_name="Slider",
            instrument_name="stepper",
            attribute_name="state",
        ),
        data=SliderState(),
    )

# Define a BatchCmds model for batch commands.
class BatchCmds(BaseModel):
    abort: bool = False
    hold: bool = False
    load: bool = False
    path: str = ""
    restart: bool = False
    start: bool = False

# Define a BatchCmdState model for batch command state.
class BatchCmdState(BaseModel):
    abort: bool = False
    hold: bool = False
    load: bool = False
    path: str = ""
    restart: bool = False
    start: bool = False
    display: str = ""
    state: int = 0

# Define a BatchUDT model that combines FullyQualifiedName and BatchCmds and BatchCmdState data.
class BatchUDT(BaseModel):
    cmd: CombinedModel[BatchCmds] = CombinedModel[BatchCmds](
        fqn=FullyQualifiedName(
            component_name="phase", instrument_name="phase", attribute_name="cmd"
        ),
        data=BatchCmds(),
    )
    state: CombinedModel[BatchCmdState] = CombinedModel[BatchCmdState](
        fqn=FullyQualifiedName(
            component_name="phase", instrument_name="phase", attribute_name="state"
        ),
        data=BatchCmdState(),
    )


### Add Environmental Sensor Models HERE ###

############################################








