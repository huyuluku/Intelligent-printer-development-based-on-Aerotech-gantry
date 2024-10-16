import tkinter as tk
from tkinter import ttk
import serial
import threading
import time
import automation1 as a1
import numpy as np

global desired_pressure_1, desired_pressure_2
serial_lock = threading.Lock()
# Initialize global variables for desired pressures
desired_pressure_1 = 15
desired_pressure_2 = 15

# Define the serial port and baud rate
arduino_port = 'COM10'  # Change to your Arduino's serial port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Allow time for Arduino to initialize
#############################################################
# -*- coding: utf-8 -*-
'''
Created on Thu Jul 13 15:24:35 2023

@author: user
'''

'''
The Automation1 console example for Python.

This example has a simple command line interface to demonstrate the basics of interacting
with an Automation1 controller from a user's perspective. The code for each command line command will
demonstrate how to perform these actions through the Python API.

The auto-complete information on the Controller class, its properties, and its methods document much of the API and how to use it.
Make sure you have an editor with auto-complete capabilities to make full use of the self-documenting auto-complete information.

This project requires the Automation1 Python API to be installed. If you haven't yet, install the "automation1" package
via pip. This can be done in this C:/Program Files/Aerotech/Automation1-MDK/APIs/Python/ folder.

For more information on installing the Automation1 Python API be sure to read the Readme.txt file in 
the C:/Program Files/Aerotech/Automation1-MDK/APIs/Python/ folder.
'''
'''
# The reference to the connected Automation1 controller. All controller interaction will be done through this object.
# The auto-complete information on this object, its properties, and its methods document much of the API and how to use it.
# This reference is None if we are not connected. See connect_to_controller() and start_controller() in this source file for
# more details on how to connect to and start the controller.
'''
def is_float(value: str):
	'''
	Determines if a string can be converted to a float.
	Args:
		value: The string value to validate.
	'''
	try:
		float(value)
		return True
	except:
		return False

def print_help():
	'''
	Prints the list of commands available to the user.
	'''
	print('Available commands:')
	print('\tConnect')
	print('\tDisconnect')
	print('\tStart')
	print('\tStop')
	print('\tEnable [Axis Name]')
	print('\tDisable [Axis Name]')
	print('\tHome [Axis Name]')
	print('\tAbort [Axis Name]')
	print('\tAxisStatus [Axis Name]')
	print('\tMoveLinear [Axis Name] [Distance] [Speed]')
	print('\tRunProgram [AeroScript Program Path]')
	print('\tProgramStatus')
	print('\tStopProgram')
	print('\tGetGlobalInteger [Index]')
	print('\tSetGlobalInteger [Index] [New Value]')
	print('\tShowAxisParameters [Axis Name]')
	print('\tQuit')

def connect_to_controller():
	'''
	Connects to the Automation1 controller.
	'''
	global controller
	if controller:
		print('Already connected')
		return

	# Calling Controller.connect() with no arguments will connect to the controller installed on
	# the local machine. If we wanted to connect to a controller installed on a different machine with
	# the IP address 192.168.1.15, we could instead call Controller.connect(host="192.168.1.15").
	#
	# Connecting to the controller will not change its running state, meaning that we might have to also
	# call Controller.start() on our controller object before we can run AeroScript programs or perform motion.
	# We must start the controller before calling any APIs under Controller.runtime. See the start_controller()
	# method in this source file for more information on starting the controller.
	controller = a1.Controller.connect()
	print('Connected to Automation1 controller')

def disconnect_from_controller():
	'''
	Disconnects from the Automation1 controller.
	'''
	global controller
	if not controller:
		print('Already disconnected')
		return
	
	# Disconnecting from a controller will not change its running state, meaning that the controller
	# might still be running after we disconnect. Call Controller.stop() before disconnecting to stop the controller from running
	# AeroScript programs or performing motion. See the stop_controller() method in this source file for more information.
	# Use this method when your application no longer needs to interact with the controller but you want the controller to continue running.
	# Since we are disconnected, our controller object is no longer usable and we should get rid of our reference to it.
	controller.disconnect()
	controller = None
	print('Disconnected from Automation1 controller')

def start_controller():
	'''
	Starts the Automation1 controller.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before you can start it')
		return

	# The act of connecting to the controller on its own will not change the running state of the controller
	# so we have to explicitly start it by calling Controller.start(). We could check Controller.is_running to
	# see if the controller is already running, but since Controller.start() will just do nothing if the
	# controller is already running we can call it regardless.
	# We must start the controller before calling any APIs under Controller.runtime.
	controller.start()
	print('Controller started')

def stop_controller():
	'''
	Stops the Automation1 controller.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before you can stop it')
		return

	# Calling Controller.stop() will stop the Automation1 controller but not disconnect us. We could check
	# Controller.is_running to see if the controller is already running, but since Controller.stop() will
	# just do nothing if the controller is already running we can call it regardless.
	controller.stop()
	print('Controller stopped')

def enable_axis(axis):
	'''
	Enables an axis.

	Args:
		axis: The name of the axis to enable.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before enabling an axis')
		return

	# We can enable an axis using the enable() method in the MotionCommands API.
	# The Commands API provides access to many of the AeroScript commands that are used to perform actions
	# on the controller.
	# 
	# Similar commands are grouped together under the top-level Commands property. For example,
	# Commands.motion provides access to the motion commands, Commands.io provides access to commands
	# for I/O operations, etc.
	#
	# If an error occurs while executing a command, like if the controller is not started or an axis fault
	# has occurred, the command will throw a ControllerException that provides information on the error.
	# See the try/except in main() for more information about handling ControllerException.
	controller.runtime.commands.motion.enable(axis)
	print(f'Axis {axis} enabled')

def disable_axis(axis):
	'''
	Disables an axis.
	Args:
		axis: The name of the axis to disable.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before disabling an axis')
		return

	# We can disable an axis using the disable() method in the MotionCommands API.
	# The Commands API provides access to many of the AeroScript commands that are used to perform actions
	# on the controller.
	# 
	# Similar commands are grouped together under the top-level Commands property. For example,
	# Commands.motion provides access to the motion commands, Commands.io provides access to commands
	# for I/O operations, etc.
	#
	# If an error occurs while executing a command, like if the controller is not started or an axis fault
	# has occurred, the command will throw a ControllerException that provides information on the error.
	# See the try/except in main() for more information about handling ControllerException.
	controller.runtime.commands.motion.disable(axis)
	print(f'Axis {axis} disabled')

def home_axis(axis):
	'''
	Homes an axis.
	Args:
		axis: The name of the axis to home.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before homing an axis')
		return

	# We can home an axis using the home() method in the MotionCommands API.
	# The Commands API provides access to many of the AeroScript commands that are used to perform actions
	# on the controller.
	# 
	# Similar commands are grouped together under the top-level Commands property. For example,
	# Commands.motion provides access to the motion commands, Commands.io provides access to commands
	# for I/O operations, etc.
	#
	# If an error occurs while executing a command, like if the controller is not started or an axis fault
	# has occurred, the command will throw a ControllerException that provides information on the error.
	# See the try/except in main() for more information about handling ControllerException.
	controller.runtime.commands.motion.home(axis)
	print(f'Axis {axis} homed')

def abort_axis(axis):
	'''
	Aborts motion on an axis.
	Args:
		axis: The name of the axis to abort.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before aborting')
		return

	# We can abort motion on an axis using the abort() method in the MotionCommands API.
	# The Commands API provides access to many of the AeroScript commands that are used to perform actions
	# on the controller.
	# 
	# Similar commands are grouped together under the top-level Commands property. For example,
	# Commands.motion provides access to the motion commands, Commands.io provides access to commands
	# for I/O operations, etc.
	#
	# If an error occurs while executing a command, like if the controller is not started or an axis fault
	# has occurred, the command will throw a ControllerException that provides information on the error.
	# See the try/except in main() for more information about handling ControllerException.
	controller.runtime.commands.motion.abort(axis)
	print(f'Motion aborted on axis {axis}')

def show_axis_status(axis):
	'''
	Gets common and important information about an axis.
	Args:
		axis: The name of the axis to get information on.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before getting an axis\'s status')
		return

	# We can get information about the current state of the controller, tasks, and axes via status items. To do so, we must first
	# specify the items we want to query by creating a StatusItemConfiguration object. We then add each status item to the axis category
	# using the axis.add() method. To actually get the values of these items, we call get_status_items(status_item_configuration), which 
	# returns a StatusItemResults object.
	status_item_configuration = a1.StatusItemConfiguration()
	# Status items are defined in enums in the Python API. ProgramPosition is the position specified in program-space, before being
	# transformed and sent to the drive. See the Controller Motion Signals help file topic for more details.
	status_item_configuration.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
	# DriveStatus is a series of bits that can be masked. We will use it to get the axis enabled bit.
	status_item_configuration.axis.add(a1.AxisStatusItem.DriveStatus, axis)
	# AxisStatus is another series of bits that can be masked. We will use it to get the axis homed bit, calibration enabled 1D bit,
	# and calibration enabled 2D bit. In this case, homed indicates whether or not the axis in question has been homed since the last
	# controller reset. The calibration bits indicate if the axis is currently calibrated.
	status_item_configuration.axis.add(a1.AxisStatusItem.AxisStatus, axis)
	result = controller.runtime.status.get_status_items(status_item_configuration)

	print(f'Axis {axis} Status')
	print('------------')

	# ProgramPosition is acquired directly as a float, which is what we need.
	program_position = result.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
	print(f'Position: {program_position}')

	# DriveStatus is a series of status bits that can be masked to get various information about the state of the drive.
	# It is acquired as a float, but we need to interpret it as a series of maskable bits. To do so, we construct an int
	# from the float value. We next apply the "Enabled" mask from the enum and check if the result equals the mask to determine
	# if the drive axis is enabled.
	drive_status = int(result.axis.get(a1.AxisStatusItem.DriveStatus, axis).value)
	is_enabled = (drive_status & a1.DriveStatus.Enabled) == a1.DriveStatus.Enabled
	print(f'Enabled: {is_enabled}')

	# AxisStatus is similar to DriveStatus in that it can be masked to get information about the state of the axis.
	# It is also acquired as a float, so we again need to interpret it as a series of maskable bits. To do so, we repeat
	# the process outlined for DriveStatus with AxisStatus.
	axis_status = int(result.axis.get(a1.AxisStatusItem.AxisStatus, axis).value)
	is_homed = (axis_status & a1.AxisStatus.Homed) == a1.AxisStatus.Homed
	print(f'Homed: {is_homed}')

	# AxisStatus also contains status bits relating to the calibration state of the axis.  To get these, we simply need to 
	# apply different masks and "or" the results.
	calibration_enabled_1D = (axis_status & a1.AxisStatus.CalibrationEnabled1D) == a1.AxisStatus.CalibrationEnabled1D
	calibration_enabled_2D = (axis_status & a1.AxisStatus.CalibrationEnabled2D) == a1.AxisStatus.CalibrationEnabled2D
	print(f'Calibration State: {calibration_enabled_1D or calibration_enabled_2D}') 

def move_axis_linear(axis, distance, speed):
	'''
	Executes a linear move on an axis.
	Args:
		axis: The name of the axis to move.
		distance: The distance to move the axis.
		speed: The speed at which to move the axis.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before moving an axis')
		return

	# The movelinear() method will not return until the move is complete.
	# We can keep this application responsive during the move if we do the move on a background thread.
	# If we change movelinear(axisName, [distance], speed) to Thread(target=movelinear, args=(axis, [distance], speed)).start(),
	# then the method will run on its own thread and we can continue doing things while the axis is moving. This requires
	# importing the "Thread" class from the "threading" module. You should be familiar with multi-threaded programming before 
	# doing this.
	print(f'Moving axis {axis}')
	controller.runtime.commands.motion.movelinear('X', [distance], speed)
	print('Move complete')

def run_program(aeroscript_program_path):
	'''
	Runs an AeroScript program on the Automation1 controller.
	Args:
		aeroscript_program_path: The path to the .ascript file to run.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before running an AeroScript program')
		return

	# When we call program.run(), it will load the program on the controller task and begin execution,
	# but it will not wait for the program to complete before returning. The AeroScript source file
	# will be compiled before running. If there is a compile error, it will throw a CompileException.
	# We can use the controller's Tasks API to check on the status of our program as it runs, and to find out when it completes.
	print('Starting AeroScript program')
	controller.runtime.tasks[1].program.run(aeroscript_program_path)

def show_program_status():
	'''
	Shows the status of the currently running AeroScript program.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before getting an AeroScript program\'s status')
		return

	# We can check the state of the task we are running the AeroScript program on (Task 1 in this example)
	# to find out the status of our running AeroScript program. We can check this task state regularly
	# to track our AeroScript program if it runs, make sure no errors occur, etc.
	# An instance of the ControllerTaskStatus class represent a moment in time for a task. To get new status you must access the status property again.
	controller_task_status = controller.runtime.tasks[1].status
	if controller_task_status.task_state == a1.TaskState.Error:
		print(f'An AeroScript error occurred: {controller_task_status.error_message}')
	elif controller_task_status.task_state == a1.TaskState.Idle:
		print('No AeroScript program is loaded or running')
	elif controller_task_status.task_state == a1.TaskState.ProgramReady:
		print('The AeroScript program has not started yet')
	elif controller_task_status.task_state == a1.TaskState.ProgramRunning:
		print('The AeroScript program is running')
	elif controller_task_status.task_state == a1.TaskState.ProgramPaused:
		print('The AeroScript program is paused')
	elif controller_task_status.task_state == a1.TaskState.ProgramComplete:
		print('The AeroScript program has completed')
	# We should not encounter these task states in this example program.
	elif controller_task_status.task_state == a1.TaskState.ProgramFeedhold:
		pass
	elif controller_task_status.task_state == a1.TaskState.Inactive:
		pass
	elif controller_task_status.task_state == a1.TaskState.Unavailable:
		pass
	elif controller_task_status.task_state == a1.TaskState.QueueRunning:
		pass
	elif controller_task_status.task_state == a1.TaskState.QueuePaused:
		pass
	else:
		pass

def stop_program():
	'''
	Stops the currently running AeroScript program.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before stopping a program')
		return

	# To stop a running AeroScript program, we stop the controller task it is running on (Task 1 in this example)
	# The call to program.stop() will terminate the program and wait for it to stop before returning.
	controller.runtime.tasks[1].program.stop()
	print('Program stopped')

def get_global_integer(index):
	'''
	Gets a value from the global integer array variable.
	Args:
		index: The index of the integer to get.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before querying a global integer')
		return

	# The controller has a set of global variable arrays that are accessible from every task on the controller and from every API.
	# These variables can be used to communicate data between tasks or between the controller and a custom application.
	# There are three global arrays for each data type: AeroScript integer values ($iglobal), AeroScript real values ($rglobal),
	# and AeroScript string values ($sglobal).
	# To get a global integer value, we use the Variables API to return a single, specific global integer index.
	# You can also get multiple global variables at once using methods like get_integers() that accepts a list of indices.
	value = controller.runtime.variables.global_.get_integer(index)
	print(f'$iglobal[{index}] is {value}')

def set_global_integer(index, new_value):
	'''
	Sets a value of an index of the global integer array variable.
	Args:
		index: The index of the integer to set.
		new_value: The new value of the integer.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before setting a global integer')
		return

	# The controller has a set of global variable arrays that are accessible from every task on the controller and from every API.
	# These variables can be used to communicate data between tasks or between the controller and a custom application.
	# There are three global arrays for each data type: AeroScript integer values ($iglobal), AeroScript real values ($rglobal), and
	# and AeroScript string values ($sglobal).
	# To change a global integer value, we use the Variables API to set a single, specific global integer index.
	# You can also set multiple global variables at once using methods like set_integers() that accepts a list of indices and new values.
	controller.runtime.variables.global_.set_integer(index, new_value)
	print(f'$iglobal[{index}] is now set to: {new_value}')

def show_axis_parameters(axis_name):
	'''
	Shows common parameter values for an axis.
	Args:
		axis_name: The axis to show parameter values for.
	'''
	# Make sure we are connected before trying to do anything.
	if not controller:
		print('You must connect to the controller before setting a global integer')
		return
		
	# Controller parameters can be accessed through the Controller.runtime.parameters property. This property is divided
	# into three categories, Axis, Task, and System. Axis and Task parameters require the use of indexers to
	# specify which axis/task the parameter value is being get/set for.
	#
	# To access a specific parameter in one of the Axis, Task, or System categories, use another indexer and provide the
	# enum value of the parameter.
	# Once a parameter is obtained, use the ".value" property to get/set its value.
	axis_fault_mask = int(controller.runtime.parameters.axes[axis_name][a1.AxisParameterId.FaultMask].value)

	# Parameters can also be accessed by properties representing groups that are based on their usage. For instance,
	# the "motion" parameter group contains the MaxJogSpeed, MaxJogDistance, and DefaultAxisRampSpeed parameters
	# since their usage all revolves around motion.
	defaultAxisSpeed = controller.runtime.parameters.axes[axis_name].motion.defaultaxisspeed.value
	defaultAxisRampRate = controller.runtime.parameters.axes[axis_name].motion.defaultaxisramprate.value

	# The FaultMask axis parameter is a series of bits that can be masked to get/set the protection status of
	# a specific axis fault. After casting the parameter value to an "int", we can and the result with 
	# our desired AxisFault enum value and compare it to itself to determine if a specified AxisFault 
	# bit is enabled.
	motorTemperatureFaultProtectionStatus = 'Enabled' if axis_fault_mask & a1.AxisFault.MotorTemperatureFault == a1.AxisFault.MotorTemperatureFault else 'Disabled'

	print(f'Motor Temperature Fault protection: {motorTemperatureFaultProtectionStatus}')
	print(f'Default Axis Speed: {defaultAxisSpeed}')
	print(f'Default Axis Ramp Rate: {defaultAxisRampRate}')

	# To set a controller parameter, use the assignment operator on the ".value" property of any controller parameter
	# to set its value.
	# Example:
	#
	# controller.runtime.parameters.axes[axis_name][AxisParameterId.DefaultAxisSpeed].value = 5.1;
	# controller.runtime.parameters.axes[axis_name].motion.defaultaxisramprate.value = 10.2;

controller = a1.Controller.connect()
controller.start()
enable_axis(['X','Y','C'])


'''
# Initialize global variables for desired pressures
desired_pressure_1 = 30
desired_pressure_2 = 30

controller = a1.Controller.connect()
controller.start()
enable_axis(['X','Y','C'])

# Define the serial port and baud rate
arduino_port = 'COM10'  # Change to your Arduino's serial port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Allow time for Arduino to initialize
'''

def close_valve(system_number):
    command = f"{system_number},-2\n"
    ser.write(command.encode())
    #write_serial_command(command)
    ser.flush()
    print(f"Closing valve {system_number}...")
    
def open_valve(system_number):
    command = f"{system_number},-1\n"
    ser.write(command.encode())
    #write_serial_command(command)
    ser.flush()
    print(f"Opening valve {system_number}...")

def set_PID_pressure(system_number, pressure):
    global desired_pressure_1, desired_pressure_2
    if pressure < 0 or pressure > 100:
        print("Pressure out of range. Must be 0 to 100 PSI.")
        return
    command = f"{system_number},{pressure}\n"
    ser.write(command.encode())
    #write_serial_command(command)
    ser.flush()
    print(f"Setting PID {system_number} to: {pressure} PSI")
    if system_number == 1:
        desired_pressure_1 = int(pressure)
    elif system_number == 2:
        desired_pressure_2 = int(pressure)

def read_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    time.sleep(0.1)  # Small delay to prevent CPU overuse

def write_serial_command(command):
    with serial_lock:
        ser.write(command.encode())
        ser.flush()
        # Wait for acknowledgment
        while True:
            if ser.readline().decode().strip() == "ACK":
                break

# Function for running the DIW printing process
def printing_process():
    global desired_pressure_1, desired_pressure_2
    '''
    nozzleDiam = 0.400
    w = 40.0
    l = 40.0
    r = 0.9*nozzleDiam
    rows = int(np.floor(l/r/2))
    z0 = 0.9*nozzleDiam
    dz= 0.9*nozzleDiam
    layers = 4
    speed = [60,60,10]
    '''
    
    set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
    set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
    time.sleep(5)
    
    open_valve(1)
    time.sleep(0.1)
    open_valve(2)
    time.sleep(0.1)
    
    move_x = 60
    move_y = 5
    move_vel = 50
    
    #controller.runtime.commands.motion.movelinear('C', [0.4], 10)
    for i in range(100):
        if np.mod(i, 2) == 0:
            for unit in range(0, 5):
                controller.runtime.commands.motion.movelinear('X', [move_x], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('Y', [move_y], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('X', [-move_x], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('Y', [move_y], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
        else:
            for unit in range(0, 5):
                controller.runtime.commands.motion.movelinear('X', [move_x], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('Y', [-move_y], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('X', [-move_x], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
                controller.runtime.commands.motion.movelinear('Y', [-move_y], move_vel)
                set_PID_pressure(1, desired_pressure_1)  # Set the PID setpoint of channel 1 to XX PSI
                set_PID_pressure(2, desired_pressure_2)  # Set the PID setpoint of channel 2 to XX PSI
        controller.runtime.commands.motion.movelinear('C', [0.4], 10)
    
    close_valve(1)
    close_valve(2)
    ser.close()
    print("Finished printing.")

# Cleanup function to ensure valves are closed and pressures are set to zero
def cleanup():
    set_PID_pressure(1, 0)
    set_PID_pressure(2, 0)
    close_valve(1)
    close_valve(2)
    ser.close()
    print("Cleaned up and closed valves.")

# UI class for controlling pressures and valves
class PressureControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pressure Control System")
        self.geometry("400x300")
        self.valve_state = {1: True, 2: True}  # Valve states: True for open, False for closed
        self.create_widgets()
        
    def create_widgets(self):
        # Valve 1 control
        self.btn_valve1 = ttk.Button(self, text="Toggle Valve 1", command=lambda: self.toggle_valve(1))
        self.btn_valve1.pack(pady=10)

        # Valve 2 control
        self.btn_valve2 = ttk.Button(self, text="Toggle Valve 2", command=lambda: self.toggle_valve(2))
        self.btn_valve2.pack(pady=10)

        # Pressure control for system 1
        ttk.Label(self, text="Pressure 1 (psi):").pack()
        self.pressure1_entry = ttk.Entry(self)
        self.pressure1_entry.pack(pady=5)
        ttk.Button(self, text="Set Pressure 1", command=self.update_desired_pressure_1).pack(pady=5)

        # Pressure control for system 2
        ttk.Label(self, text="Pressure 2 (psi):").pack()
        self.pressure2_entry = ttk.Entry(self)
        self.pressure2_entry.pack(pady=5)
        ttk.Button(self, text="Set Pressure 2", command=self.update_desired_pressure_2).pack(pady=5)

    def update_desired_pressure_1(self):
        global desired_pressure_1
        try:
            desired_pressure_1 = int(self.pressure1_entry.get())
            print(f"Updated desired pressure for system 1 to: {desired_pressure_1} PSI")
        except ValueError:
            print("Invalid input for pressure 1")

    def update_desired_pressure_2(self):
        global desired_pressure_2
        try:
            desired_pressure_2 = int(self.pressure2_entry.get())
            print(f"Updated desired pressure for system 2 to: {desired_pressure_2} PSI")
        except ValueError:
            print("Invalid input for pressure 2")

    def toggle_valve(self, valve_number):
        state = self.valve_state[valve_number]
        if state:
            close_valve(valve_number)
            self.valve_state[valve_number] = False
            text = "Open Valve " + str(valve_number)
        else:
            open_valve(valve_number)
            self.valve_state[valve_number] = True
            text = "Close Valve " + str(valve_number)
        if valve_number == 1:
            self.btn_valve1.config(text=text)
        else:
            self.btn_valve2.config(text=text)

# Start the printing process in a separate thread
threading.Thread(target=printing_process, daemon=True).start()

if __name__ == "__main__":
    # Initialize and run the UI
    app = PressureControlApp()
    
    def on_closing():
        cleanup()
        app.destroy()
        ser.close()
    
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
    # Ensure serial connection is closed when the application is closed
    ser.close()
