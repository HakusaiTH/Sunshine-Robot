import datetime

def add_timestamp_to_filename(filename):
    # Get the current date and time
    current_time = datetime.datetime.now()
    # Format the date and time as a string
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # Concatenate the timestamp with the filename
    new_filename = f"{filename.split('.')[0]}_{timestamp}.jpg"
    return new_filename