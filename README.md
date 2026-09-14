# Alarm Clock

A simple command-line alarm clock built with Python.

## Requirements

- Python 3.10+
- No database
- No external dependencies

## Run

```bash
python alarm.py

Command	Description
add HH:MM	Add a new alarm
list	List all alarms
enable ID	Enable an alarm
disable ID	Disable an alarm
delete ID	Delete an alarm
run	Start the alarm clock
help	Show available commands
exit	Exit the application

$ python alarm.py

Alarm Clock - type 'help' for commands

> add 15:30
Alarm 1 set for 15:30

> list
1: 15:30 (enabled)

> run
Alarm clock running. Press Ctrl+C to stop.

*** ALARM 1 - 15:30 ***

Behavior
Uses 24-hour HH:MM format.
If an alarm time has already passed today, it is scheduled for the next day.
Alarms are one-time and are disabled after ringing.
Alarm data is stored in memory and is lost when the application exits.
Ctrl+C safely stops the alarm clock