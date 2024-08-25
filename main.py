from datetime import datetime, timedelta
import pygame
import time
import threading

class Utils:
    SNOOZE_DURATION = 5  # In minutes

    @staticmethod
    def add_minutes(time_string):
        try:
            time_format = "%I:%M %p"
            time_obj = datetime.strptime(time_string, time_format)
            new_time_obj = time_obj + timedelta(minutes=Utils.SNOOZE_DURATION)        
            return new_time_obj.strftime(time_format)
        except ValueError:
            print("\n\tError: Invalid time format for snooze.")
            return None

    @staticmethod
    def validate_time(hour, minute, time_period):
        return (1 <= hour <= 12) and (0 <= minute <= 59) and (time_period in {"AM", "PM"})

    @staticmethod
    def validate_day_of_week(day_of_week):
        valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
        return day_of_week in valid_days

class Alarm:
    def __init__(self, time, day_of_week):
        self._time = time
        self._day_of_week = day_of_week
        self._snooze_count = 0
    
    def get_time(self):
        return self._time
    
    def set_time(self, new_time):
        self._time = new_time
    
    def get_day_of_week(self):
        return self._day_of_week
    
    def increase_snooze_count(self):
        self._snooze_count += 1
    
    def get_snooze_count(self):
        return self._snooze_count
    
    def get_alarm_details(self):
        return f"{self._time} - {self._day_of_week}"
    
    def __str__(self):
        return f"\n\tAlarm is set for {self.get_alarm_details()}"

class AlarmClock:
    def __init__(self):
        self._alarms = []
        self._running = True
        self._is_alarm_on = False
        self._curr_alarm_idx = None
        self._initialize_pygame()

    def _initialize_pygame(self):
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"\n\tError initializing Pygame mixer: {e}")
            self._running = False

    def add_alarm(self):
        try:
            hour, minute, time_period, day_of_week = self._get_alarm_input()
            if self._validate_alarm_input(hour, minute, time_period, day_of_week):
                alarm = Alarm(f"{hour:02d}:{minute:02d} {time_period}", day_of_week)
                if alarm in self._alarms:
                    print(alarm)
                    return
                self._alarms.append(alarm)
                print(alarm)
        except ValueError:
            print("\n\tError: Invalid input. Please enter numeric values for hour and minute.")
        except Exception as e:
            print(f"\n\tUnexpected error: {e}")

    def _get_alarm_input(self):
        hour = int(input("Enter hour (1-12): "))
        minute = int(input("Enter minute (0-59): "))
        time_period = input("Enter period (AM/PM): ").upper()
        day_of_week = input("Enter day of the week (Monday - Sunday): ").capitalize()
        return hour, minute, time_period, day_of_week

    def _validate_alarm_input(self, hour, minute, time_period, day_of_week):
        if not Utils.validate_time(hour, minute, time_period):
            print("\n\tError: Invalid time format.")
            return False
        if not Utils.validate_day_of_week(day_of_week):
            print("\n\tError: Invalid day of the week.")
            return False
        return True

    def delete_alarm(self):
        if not self._alarms:
            print("\n\tNo active alarms to delete.")
            return 
        self.display_alarms()
        try:
            idx = int(input("Enter alarm number to delete: ")) - 1
            self._delete_alarm_by_index(idx)
        except ValueError:
            print("\n\tError: Invalid input. Please enter a numeric value.")

    def _delete_alarm_by_index(self, idx):
        if 0 <= idx < len(self._alarms):
            self._alarms.pop(idx)
            print(f"Alarm deleted.")
        else:
            print("\n\tError: Invalid alarm number.")

    def display_alarms(self):
        if not self._alarms:
            print("\n\tNo active alarms to display")
            return 
        print("\nActive Alarms: ")
        for idx, alarm in enumerate(self._alarms):
            print(f"\t{idx+1}) {alarm.get_alarm_details()}")
    
    def snooze_alarm(self):
        if self._curr_alarm_idx is not None:
            alarm = self._alarms[self._curr_alarm_idx]
            print("Snoozing alarm...")
            new_time = Utils.add_minutes(alarm.get_time())
            if new_time:
                alarm.set_time(new_time)
                alarm.increase_snooze_count()
                print(f"Alarm snoozed until {alarm.get_alarm_details()}")

    def play_alarm_sound(self):
        try:
            pygame.mixer.music.load("alarm_sound.mp3")
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"\n\tError loading or playing alarm sound: {e}")

    def stop_alarm_sound(self):
        pygame.mixer.music.stop()

    def handle_alarm(self, choice):
        if self._is_alarm_on:
            alarm = self._alarms[self._curr_alarm_idx]
            if alarm.get_snooze_count() == 3:
                self._delete_alarm_by_index(self._curr_alarm_idx)
            else:
                self.stop_alarm_sound()
                self.snooze_alarm()

                if input("Enter 'off' to delete the alarm or press enter: ") == "off":
                    self._delete_alarm_by_index(self._curr_alarm_idx)

            self._is_alarm_on = False
            self._curr_alarm_idx = None

    def check_for_alarm(self):
        while self._running:
            try:
                current_time = datetime.now().strftime(f"%I:%M %p - %A")
                for idx, alarm in enumerate(self._alarms):
                    if alarm.get_alarm_details() == current_time:
                        self._is_alarm_on = True
                        self._curr_alarm_idx = idx
                        print("\n\tPress Enter to snooze the alarm.")
                        self.play_alarm_sound()
                        break
            except Exception as e:
                print(f"\n\tError checking for alarms: {e}")

            time.sleep(3)

    def run(self):
        try:
            alarm_thread = threading.Thread(target=self.check_for_alarm)
            alarm_thread.start()

            while True:
                current_time = datetime.now().strftime(f"%I:%M %p - %A")

                print("\n-----------------------")
                print(f"Time: {current_time}")
                print("-----------------------")

                print("\nOptions:")
                print("\t1. Alarm Settings")
                print("\t2. Exit")

                user_choice = input("Choose an option (1/2): ")

                if self._is_alarm_on:
                    self.handle_alarm(user_choice)
                    continue

                if user_choice == "1":
                    self._pause_alarm_thread(alarm_thread)

                    print("\n Alarm Settings:")
                    print("\t1. Add Alarm")
                    print("\t2. Delete Alarm")
                    print("\t3. Display Alarms")
                    choice = input("Choose an option (1-3): ")

                    if choice == "1":
                        self.add_alarm()
                    elif choice == "2":
                        self.delete_alarm()
                    elif choice == "3":
                        self.display_alarms()
                    else:
                        print("Invalid choice. Please try again.")

                    self._resume_alarm_thread()

                elif user_choice == "2":
                    self._stop_alarm_thread(alarm_thread)
                    break
                else:
                    print("\n\tError: Invalid Input")
        except Exception as e:
            print(f"\n\tUnexpected error: {e}")

    def _pause_alarm_thread(self, alarm_thread):
        self._running = False
        alarm_thread.join()  

    def _resume_alarm_thread(self):
        self._running = True
        alarm_thread = threading.Thread(target=self.check_for_alarm)
        alarm_thread.start()

    def _stop_alarm_thread(self, alarm_thread):
        self._running = False
        alarm_thread.join()

if __name__ == "__main__":
    alarm_clock = AlarmClock()
    alarm_clock.run()
