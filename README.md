# Training ENS

This repository holds the ENS Package for the Beta Training Course Example Package. It contains an App Task, IO Task and Views.

It is currently running on Framework Version -- Edge, Runtime (TBA, system is currently offline).

The scope of this ENS is to teach individuals how to use our software by communicating simple control logic to a stepper and distance sensor. While the system is running the stepper motoro will move the linear rail 20000 steps forward, pause for 5 seconds, and return 20000 steps to its original position.

## App Task

The App Task contains a simple state machine with the following states: Main Routine, Idle Routine, Running Routine, Return Routine, and an Abort Routine.
