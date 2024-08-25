# Interactive Command-Line Alarm Clock

This Python-based command-line application serves as an interactive alarm clock. It displays the current time, allows users to create and manage alarms, and features snooze functionality. 

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Sample Screenshots](#sample-screenshots)
4. [Usage Instructions](#usage-instructions)


## Features

- **Display Current Time**: The application continuously displays the current time in the format `HH:MM AM/PM - Day of the Week`.
- **Create Alarms**: Users can create any number of alarms by specifying the time, AM/PM period, and the day of the week.
- **Snooze Functionality**: Users can snooze an alarm up to 3 times, with each snooze lasting 5 minutes.
- **Delete Alarms**: Users can delete any existing alarm.

## Requirements

- Python 3.x
- Pygame library for sound playback

You can install the required Pygame library using:

```bash
pip install pygame
```

## Sample Screenshots


## Usage Instructions

### Add Alarm:
1. Choose the "Alarm Settings" option.
2. Select "Add Alarm."
3. Enter the hour, minute, AM/PM period, and day of the week when prompted.
4. The new alarm will be added to the list of active alarms.

### Snooze Alarm:
1. When an alarm rings, press Enter to snooze the alarm.
2. The alarm will be snoozed for 5 minutes, up to a maximum of 3 times.

### Delete Alarm:
1. Choose the "Alarm Settings" option.
2. Select "Delete Alarm."
3. Choose the alarm you want to delete by entering the corresponding number.

### Display Alarms:
1. Choose the "Alarm Settings" option.
2. Select "Display Alarms."
3. The application will show all currently active alarms.

### Exit Application:
1. Choose the "Exit" option from the main menu.

## Notes:
- The alarm sound will play when the set time and day are reached.
- Ensure that the `alarm_sound.mp3` file is present in the same directory as the script for the alarm sound to play.

