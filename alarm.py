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

    for alarm in alarms:
        status = "enabled" if alarm["enabled"] else "disabled"
        print(f"{alarm['id']}: {alarm['time']:%H:%M} ({status})")


def find_alarm(alarm_id):
    return next((a for a in alarms if a["id"] == alarm_id), None)


def set_enabled(alarm_id, enabled):
    alarm = find_alarm(alarm_id)

    if not alarm:
        raise ValueError(f"Alarm {alarm_id} not found")

    alarm["enabled"] = enabled
    print(f"Alarm {alarm_id} {'enabled' if enabled else 'disabled'}")


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

        alarm_time = datetime.combine(now.date(), alarm["time"])

        if alarm_time <= now:
            alarm_time += timedelta(days=1)

        result.append((alarm, alarm_time))

    return min(result, key=lambda x: x[1]) if result else None


def run():
    print("Alarm clock running. Press Ctrl+C to stop.")

    while True:
        result = get_next_alarm()

        if not result:
            time.sleep(2)
            continue

        alarm, alarm_time = result
        remaining = (alarm_time - datetime.now()).total_seconds()

        if remaining > 0:
            time.sleep(min(remaining, 1))
            continue

        print(f"\n*** ALARM {alarm['id']} - {alarm['time']:%H:%M} ***")
        print("\a")
        alarm["enabled"] = False


def help():
    print("""
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

            if command in ("exit", "quit"):
                break

            if command == "list":
                list_alarms()
                continue

            if command == "run":
                run()
                continue

            if command == "help":
                help()
                continue

            parts = command.split()

            if len(parts) != 2:
                print("Invalid command. Type 'help'.")
                continue

            action, value = parts
            alarm_id = int(value) if action != "add" else None

            if action == "add":
                add_alarm(value)
            elif action == "enable":
                set_enabled(alarm_id, True)
            elif action == "disable":
                set_enabled(alarm_id, False)
            elif action == "delete":
                delete_alarm(alarm_id)
            else:
                print("Unknown command.")

        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
