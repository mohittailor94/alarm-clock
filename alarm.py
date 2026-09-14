import time
import threading
from datetime import datetime, timedelta

alarms = []
next_id = 1
alarm_thread = None
running = False


def add_alarm(value):
    global next_id

    try:
        alarm_time = datetime.strptime(value, "%H:%M").time()
    except ValueError:
        raise ValueError("Use HH:MM format")

    alarms.append({
        "id": next_id,
        "time": alarm_time,
        "enabled": True
    })

    print(f"Alarm {next_id} set for {value}")
    next_id += 1
    
    # Restart alarm thread when alarm is added
    start_alarm_thread()


def list_alarms():
    if not alarms:
        print("No alarms set.")
        return

    print()
    print("+------+-------+----------+")
    print("| ID   | Time  | Status   |")
    print("+------+-------+----------+")

    for alarm in alarms:
        status = "Enabled" if alarm["enabled"] else "Disabled"

        print(
            f"| {alarm['id']:<4} "
            f"| {alarm['time']:%H:%M} "
            f"| {status:<8} |"
        )

    print("+------+-------+----------+")
    print()


def find_alarm(alarm_id):
    return next(
        (alarm for alarm in alarms if alarm["id"] == alarm_id),
        None
    )


def set_enabled(alarm_id, enabled):
    alarm = find_alarm(alarm_id)

    if not alarm:
        raise ValueError(f"Alarm {alarm_id} not found")

    alarm["enabled"] = enabled

    status = "enabled" if enabled else "disabled"
    print(f"Alarm {alarm_id} {status}")
    
    # Restart alarm thread when alarm is enabled
    if enabled:
        start_alarm_thread()


def delete_alarm(alarm_id):
    alarm = find_alarm(alarm_id)

    if not alarm:
        raise ValueError(f"Alarm {alarm_id} not found")

    alarms.remove(alarm)

    print(f"Alarm {alarm_id} deleted")
    
    # Restart alarm thread if there are still enabled alarms
    if any(alarm["enabled"] for alarm in alarms):
        start_alarm_thread()


def get_next_alarm():
    now = datetime.now()
    result = []

    for alarm in alarms:

        if not alarm["enabled"]:
            continue

        alarm_time = datetime.combine(
            now.date(),
            alarm["time"]
        )

        # If today's alarm time has already passed,
        # schedule it for tomorrow.
        if alarm_time <= now:
            alarm_time += timedelta(days=1)

        result.append((alarm, alarm_time))

    if not result:
        return None

    return min(
        result,
        key=lambda x: x[1]
    )


def start_alarm_thread():
    global alarm_thread, running
    
    # Only start a new thread if the current one is not alive
    if alarm_thread is None or not alarm_thread.is_alive():
        alarm_thread = threading.Thread(target=run, daemon=True)
        alarm_thread.start()


def run():
    global running
    running = True
    print("\nAlarm clock running in background. Press Ctrl+C to exit.\n")

    while running:
        result = get_next_alarm()

        # No enabled alarms - stop running
        if not result:
            # Check if there are any alarms at all or all are disabled
            if not alarms or all(not alarm["enabled"] for alarm in alarms):
                running = False
                break
            time.sleep(1)
            continue

        alarm, alarm_time = result

        remaining = (
            alarm_time - datetime.now()
        ).total_seconds()

        # Wait until alarm time.
        # Sleep maximum 1 second so that
        # the alarm triggers accurately.
        if remaining > 1:
            time.sleep(min(remaining, 1))
            continue

        # Alarm triggered
        print()
        print(
            f"*** ALARM {alarm['id']} - "
            f"{alarm['time']:%H:%M} ***"
        )
        print("\a")

        # Disable alarm after triggering
        alarm["enabled"] = False


def show_help():
    print("""
Available commands:

add HH:MM       Add alarm
list            List alarms
enable ID       Enable alarm
disable ID      Disable alarm
delete ID       Delete alarm
help            Show commands
exit            Quit
""")


def main():
    global alarm_thread, running
    
    print("Alarm Clock - type 'help' for commands")
    
    # Start alarm thread automatically
    start_alarm_thread()

    while True:
        try:
            command = input("> ").strip()

            if not command:
                continue

            # Exit
            if command in ("exit", "quit"):
                print("Goodbye.")
                running = False
                break

            # Commands without arguments
            if command == "list":
                list_alarms()
                continue

            if command == "help":
                show_help()
                continue

            parts = command.split()

            if len(parts) != 2:
                print("Invalid command. Type 'help'.")
                continue

            action, value = parts

            # Add alarm
            if action == "add":
                add_alarm(value)

            # Commands requiring ID
            elif action in ("enable", "disable", "delete"):

                try:
                    alarm_id = int(value)
                except ValueError:
                    print("Error: ID must be a number.")
                    continue

                if action == "enable":
                    set_enabled(alarm_id, True)

                elif action == "disable":
                    set_enabled(alarm_id, False)

                elif action == "delete":
                    delete_alarm(alarm_id)

            else:
                print("Unknown command. Type 'help'.")

        except ValueError as e:
            print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nGoodbye.")
            running = False
            break


if __name__ == "__main__":
    main()
