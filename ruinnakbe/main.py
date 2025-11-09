import datetime

def get_current_timestamp():
  """Gets the current timestamp and formats it."""
  now = datetime.datetime.now()
  formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
  return formatted_timestamp

if __name__ == "__main__":
  timestamp = get_current_timestamp()
  print(f"Current Timestamp: {timestamp}")
