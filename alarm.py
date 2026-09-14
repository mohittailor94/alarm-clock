import time
from datetime import datetime, timedelta

alarms = []
next_id = 1


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


def delete_alarm(alarm_id):
    alarm = find_alarm(alarm_id)

    if not alarm:
        raise ValueError(f"Alarm {alarm_id} not found")

    alarms.remove(alarm)

    print(f"Alarm {alarm_id} deleted")


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


def run():
    print("Alarm clock running. Press Ctrl+C to stop.")

    while True:
        result = get_next_alarm()

        # No enabled alarms
        if not result:
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
run             Start alarm clock
help            Show commands
exit            Quit
""")


def main():
    print("Alarm Clock - type 'help' for commands")

    while True:
        try:
            command = input("> ").strip()

            if not command:
                continue

            # Exit
            if command in ("exit", "quit"):
                print("Goodbye.")
                break

            # Commands without arguments
            if command == "list":
                list_alarms()
                continue

            if command == "run":
                run()
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
            break


if __name__ == "__main__":
    main()
