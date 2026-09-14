# Alarm Clock

A simple command-line alarm clock built with Python that runs alarms in the background.

## Requirements

- Python 3.10+
- No database
- No external dependencies

## Run

```bash
python alarm.py
```

## Commands

| Command | Description |
|---------|-------------|
| `add HH:MM` | Add a new alarm |
| `list` | List all alarms |
| `enable ID` | Enable an alarm |
| `disable ID` | Disable an alarm |
| `delete ID` | Delete an alarm |
| `help` | Show available commands |
| `exit` | Exit the application |

## Features

- **Automatic Background Running** - The alarm clock automatically starts in the background when you run the application
- **Dynamic Alarm Management** - Add, enable, disable, or delete alarms at any time while the clock is running
- **Auto Thread Restart** - When you add a new alarm or enable a disabled alarm, the alarm thread automatically restarts
- **Smart Stop** - The alarm thread stops automatically when there are no enabled alarms
- **Live Updates** - View and manage your alarms in real-time without stopping the application

## Usage Example

```bash
$ python alarm.py

Alarm Clock - type 'help' for commands

Alarm clock running in background. Press Ctrl+C to exit.

> add 15:30
Alarm 1 set for 15:30

> add 16:45
Alarm 2 set for 16:45

> list
+------+-------+----------+
| ID   | Time  | Status   |
+------+-------+----------+
| 1    | 15:30 | Enabled  |
| 2    | 16:45 | Enabled  |
+------+-------+----------+

> disable 2
Alarm 2 disabled

> enable 2
Alarm 2 enabled
Alarm clock running in background. Press Ctrl+C to exit.

*** ALARM 1 - 15:30 ***

> exit
Goodbye.
```

## Behavior

- Uses 24-hour HH:MM format
- If an alarm time has already passed today, it is scheduled for the next day
- Alarms are one-time and are disabled after ringing
- Alarm data is stored in memory and is lost when the application exits
- Press Ctrl+C or type `exit` to stop the application
- The alarm thread automatically stops when all alarms are disabled or deleted