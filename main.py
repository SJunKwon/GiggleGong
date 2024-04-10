import sys, io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
import eel
import datetime
import winsound  # for Windows, for other platforms you might need to use other libraries
import threading
import os
import base64
import pygame
import uuid  # for generating unique identifiers
import csv
import ast  # Module to safely evaluate literal expressions

# Initialize Eel
eel.init('app', allowed_extensions=['.html', '.css', '.png', '.ico', '.mp3'])

alarms = []
# File path for the CSV file
CSV_FILE = 'saves/alarms.csv'
current_alarm = None
stop_beep = False

def load_alarms_from_csv():
    global alarms
    alarms = []  # Clear the existing alarms list before loading from the file
    # Function to convert string representation of boolean to actual boolean value
    def str_to_bool(s):
        return s.lower() in ['true', '1']
    try:
        with open(CSV_FILE, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse the 'days' string as a list
                days_list = ast.literal_eval(row['days'])
                alarms.append({
                    'name': row['name'],
                    'time': row['time'],
                    'days': days_list,  # Use the parsed list
                    'cstm_msg': row['cstm_msg'],
                    'musicFile': row['musicFile'],
                    'active': str_to_bool(row['active']),  # Convert string to boolean
                    'triggered': str_to_bool(row['triggered'])  # Convert string to boolean
                })
        print("Alarms loaded successfully from CSV file.")
        print(alarms)
    except FileNotFoundError:
        print("CSV file not found. No alarms loaded.")

# Call the function to load alarms when the program starts
load_alarms_from_csv()

@eel.expose
def add_alarm(name, time, days, cstm_msg, music_file):
    global alarms
    if music_file:
        # Decode the base64 string to binary data
        music_data = base64.b64decode(music_file)
        # Generate a unique file name
        musicFile = str(uuid.uuid4()) + ".mp3"  # You can use any suitable extension here
        # Specify the directory to save the music file
        music_directory = 'saves/alarm_music'
        # Ensure the directory exists, create it if it doesn't
        if not os.path.exists(music_directory):
            os.makedirs(music_directory)
        # Save the music data to a file
        music_file_path = os.path.join(music_directory, musicFile)
        # Save the music data to a file
        with open(music_file_path, 'wb') as f:
            f.write(music_data)
        # Store the file path in the alarms dictionary
        alarm = {'name': name, 'time': time, 'days': days, 'cstm_msg': cstm_msg, 'musicFile': musicFile, 'active': True, 'triggered': False}
    else:
        alarm = {'name': name, 'time': time, 'days': days, 'cstm_msg': cstm_msg, 'musicFile': None, 'active': True, 'triggered': False}

    alarms.append(alarm)
    print(f"Alarm added: {name}, Time: {time}, Days: {days}, Custom Message: {cstm_msg}, Music File: {music_file}")
    
    # Save the alarms to a CSV file
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['name', 'time', 'days', 'cstm_msg', 'musicFile', 'active', 'triggered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(alarm)
    
    return "Alarm added successfully"

@eel.expose
def check_alarms():
    current_time = datetime.datetime.now().strftime("%H:%M") # Get current time (e.g Hour:Minute)
    current_day = datetime.datetime.now().strftime("%a")  # Get the current day (e.g., Mon, Tue)

    for alarm in alarms:
        if alarm['active'] and alarm['time'] == current_time and current_day in alarm['days'] and not alarm['triggered']:
            trigger_alarm(alarm)

@eel.expose
def get_alarms():
    return alarms

@eel.expose
def edit_alarms(index, name, time, days, cstm_msg, musicFile, active, triggered):
    # Get the previous music file associated with the alarm
    previous_music_file = alarms[index]['musicFile']

    if musicFile:
        # Decode the base64 string to binary data
        music_data = base64.b64decode(musicFile)
        # Generate a unique file name
        musicFile = str(uuid.uuid4()) + ".mp3"  # You can use any suitable extension here
        # Specify the directory to save the music file
        music_directory = 'saves/alarm_music'
        # Ensure the directory exists, create it if it doesn't
        if not os.path.exists(music_directory):
            os.makedirs(music_directory)
        # Save the music data to a file
        music_file_path = os.path.join(music_directory, musicFile)
        # Save the music data to a file
        with open(music_file_path, 'wb') as f:
            f.write(music_data)

        # Delete the previous music file if it exists
        if previous_music_file:
            previous_music_file_path = os.path.join(music_directory, previous_music_file)
            if os.path.exists(previous_music_file_path):
                os.remove(previous_music_file_path)
                
        # Update the alarms list with the edited alarm
        alarms[index] = {'name': name,'time': time, 'days': days, 'cstm_msg': cstm_msg, 'musicFile': musicFile, 'active': active, 'triggered': triggered}
    else:
        alarms[index] = {'name': name, 'time': time, 'days': days, 'cstm_msg': cstm_msg, 'musicFile': None, 'active': True, 'triggered': False}
        music_directory = 'saves/alarm_music'
        # Delete the previous music file if it exists
        if previous_music_file:
            previous_music_file_path = os.path.join(music_directory, previous_music_file)
            if os.path.exists(previous_music_file_path):
                os.remove(previous_music_file_path)
    
    # Rewrite the entire CSV file with the updated alarm information
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['name', 'time', 'days', 'cstm_msg', 'musicFile', 'active', 'triggered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(alarms)
    
    return "Alarm edited successfully"

@eel.expose
def del_alarms(index):
    global alarms
    alarm_to_delete = alarms[index]
    # Check if the alarm has an associated music file
    if alarm_to_delete['musicFile']:
        music_filename = alarm_to_delete['musicFile']
        music_file_path = os.path.join('saves', 'alarm_music', music_filename)
        # Delete the music file
        try:
            os.remove(music_file_path)
            print(f"Deleted music file: {music_file_path}")
        except FileNotFoundError:
            print(f"Music file not found: {music_file_path}")
    del alarms[index]
    
    # Rewrite the entire CSV file without the deleted alarm
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['name', 'time', 'days', 'cstm_msg', 'musicFile', 'active', 'triggered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(alarms)
    
    return alarms

@eel.expose
def get_current_alarm():
    global current_alarm
    return current_alarm

def trigger_alarm(alarm):
    global current_alarm
    current_alarm = alarm
    eel.show('game.html')
    global stop_beep
    stop_beep = False
    if alarm['musicFile']:
        threading.Thread(target=play_music, args=(alarm['musicFile'],)).start()
    else:
        threading.Thread(target=play_beep_sound).start()
    print(f"Alarm ringing: {alarm['time']}")
    alarm['triggered'] = True

@eel.expose
def play_music(musicFile):
    global stop_beep
    pygame.mixer.init()
    music_dir = 'saves/alarm_music'
    music_path = os.path.join(music_dir, musicFile)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)
    while not stop_beep:
        if musicFile:
            try:
                pygame.time.Clock().tick(10)  # Adjust the playback speed if necessary
            except Exception as e:
                print(f"Error playing music: {e}")
        else:
            print("No music file provided for the alarm.")

# Expose a function to stop playing the beep sound
@eel.expose
def play_beep_sound():
    while not stop_beep:
        winsound.Beep(1000, 1000)

# Expose a function to stop playing the beep sound
@eel.expose
def stop_beep_sound():
    global stop_beep
    stop_beep = True
    if not pygame.get_init():
        pygame.mixer.music.stop()  # Stop the music
        pygame.mixer.quit()
    else:
        print("Pygame is not initialized.")

# Function to reset the alarm state after a delay
@eel.expose
def reset_alarm_state_delayed(alarm):
    def reset():
        print("Alarm dictionary:", alarm)
        alarm['triggered'] = False
        print(f"Alarm state reset for {alarm['time']} after delay")

    # Schedule the reset after a delay of 1 minute (adjust as needed)
    delay = 60  # 60 seconds = 1 minute
    threading.Timer(delay, reset).start()

@eel.expose
def game_check():
    eel.show('game.html')

'''
def exit_program():
    global reset_initated
    print("Exiting the program...")
    stop_beep_sound()  # Stop any background audio
    # Perform other shutdown actions as needed
    if reset_initated == False:
        sys.exit
'''
if __name__ == '__main__':
    eel.start('index.html', mode="chromePort", size=(800, 600))
