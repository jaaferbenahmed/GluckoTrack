import csv
from datetime import datetime
import os 
from tabulate import tabulate
import statistics

# --- Constants ---

NORMAL_BS_MIN = 70
NORMAL_BS_MAX = 139 
DATA_FILE = "data.csv"
HEADERS = ["Timestamp", "Blood Glucose (mg/dL)", "State"] 


def add_reading_flow():
    """Guides the user through adding a new reading."""
    print("\n--- Add New Reading ---")
    bs_value = get_blood_sugar_input()
    timestamp = get_current_datetime_str()
    state = get_state(bs_value)
    
    print(f"Reading: {bs_value} mg/dL, State: {state}, Time: {timestamp}")
    save_new_reading(bs_value, state, timestamp)

def get_blood_sugar_input():
    """"Gets Blood Sugar Value from the user."""
    while True:
        try:
            bs_str = input("Enter your blood sugar level (mg/dL): ")
            bs_value = float(bs_str) 

            if bs_value <= 0: 
                print("Blood sugar level must be a positive number.")
                continue
            return bs_value
        except ValueError:
            print("Invalid input. Please enter a numerical value for your blood sugar.")

def get_state(blood_sugar_reading):
    """"Classifies the state based on the blood sugar reading."""
    if blood_sugar_reading < NORMAL_BS_MIN:
        return "Low"
    elif NORMAL_BS_MIN <= blood_sugar_reading <= NORMAL_BS_MAX:
        return "Normal"
    else: 
        return "High"

def get_current_datetime_str():
    """Gets current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

def load_data():
    """Loads all data from the CSV file."""
    data = []
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return data # Return empty list if file doesn't exist or is empty

    try:
        with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader) 
            if header != HEADERS:
                print(f"Warning: CSV header mismatch. Expected {HEADERS}, Got {header}. Data might be misaligned.")
            
            for row in reader:
                try:
                    row[1] = float(row[1])
                    data.append(row)
                except (ValueError, IndexError):
                    print(f"Skipping malformed row: {row}")
                    continue
        return data
    except Exception as e:
        print(f"Error loading data: {e}. Returning empty data set.")
        return []

def save_new_reading(blood_sugar, state, timestamp):
    """Saves a single new reading to the CSV file."""
    file_exists = os.path.exists(DATA_FILE)
    file_is_empty = not file_exists or os.stat(DATA_FILE).st_size == 0

    try:
        with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file_is_empty:
                writer.writerow(HEADERS)
            writer.writerow([timestamp, blood_sugar, state])
        print("Reading successfully saved.")
    except Exception as e:
        print(f"Error saving data: {e}")

def display_all_readings():
    """Displays all blood sugar readings using tabulate."""
    all_data = load_data()

    if not all_data:
        print("\nNo blood sugar readings recorded yet.")
        return

    print("\n--- All Blood Sugar Readings ---")
    display_rows = [[row[0], f"{row[1]:.1f}", row[2]] for row in all_data] 
    print(tabulate(display_rows, headers=HEADERS, tablefmt="grid"))
    print("--------------------------------\n")

def get_monthly_summary_data(year, month):
    """
    Calculates summary statistics for a given month and year.
    Returns a dictionary with 'avg', 'min', 'max', 'normal_count', 'low_count', 'high_count'.
    """
    all_data = load_data()
    monthly_readings = []
    
    for row in all_data:
        try:
            
            record_datetime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            if record_datetime.year == year and record_datetime.month == month:
                monthly_readings.append(row[1]) 
        except (ValueError, IndexError):
            
            continue

    if not monthly_readings:
        return None 

    avg_bs = statistics.mean(monthly_readings)
    min_bs = min(monthly_readings)
    max_bs = max(monthly_readings)

    normal_count = 0
    low_count = 0
    high_count = 0

    for bs_value in monthly_readings:
        state = get_state(bs_value)
        if state == "Normal":
            normal_count += 1
        elif state == "Low":
            low_count += 1
        else: 
            high_count += 1
            
    total_readings = len(monthly_readings)
    
    return {
        "avg": avg_bs,
        "min": min_bs,
        "max": max_bs,
        "normal_count": normal_count,
        "low_count": low_count,
        "high_count": high_count,
        "total_readings": total_readings,
    }

def display_monthly_summary_flow():
    """Guides the user through viewing a monthly summary."""
    print("\n--- View Monthly Summary ---")
    while True:
        try:
            year_str = input("Enter year (YYYY): ")
            month_str = input("Enter month (1-12): ")
            year = int(year_str)
            month = int(month_str)

            if not (1 <= month <= 12)  :
                print("Invalid month. Please try again.")
                continue
            if not(1900 <= year <= datetime.now().year + 1): 
                print("Invalid year. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter numbers for year and month.")

    summary = get_monthly_summary_data(year, month)

    if summary:
        print(f"\n--- Summary for {datetime(year, month, 1).strftime('%B %Y')} ---")
        summary_table = [
            ["Average Blood Sugar", f"{summary['avg']:.1f} mg/dL"],
            ["Minimum Blood Sugar", f"{summary['min']:.1f} mg/dL"],
            ["Maximum Blood Sugar", f"{summary['max']:.1f} mg/dL"],
            ["Total Readings", summary['total_readings']],
            ["Normal Readings", summary['normal_count']],
            ["Low Readings", summary['low_count']],
            ["High Readings", summary['high_count']],
        ]
        print(tabulate(summary_table, tablefmt="grid"))
        # Add basic health advice based on summary (simple version)
        if summary['high_count'] > summary['total_readings'] * 0.3: # More than 30% high readings
            print("\nConsider discussing consistently high readings with your doctor.")
        elif summary['low_count'] > summary['total_readings'] * 0.1: # More than 10% low readings
             print("\nBe mindful of low readings. Ensure regular meal times and consult your doctor if frequent.")
        elif summary['normal_count'] > summary['total_readings'] * 0.9 and summary['total_readings'] > 0:
            print("\nExcellent! Your blood sugar levels are consistently within the normal range this month.")
        print("------------------------------------------\n")
    else:
        print(f"\nNo blood sugar readings found for {datetime(year, month, 1).strftime('%B %Y')}.")

# Main Program 

def main():
    """Displays the main menu and handles user choices."""
    while True:
        print("--- Blood Sugar Tracker Menu ---")
        print("1. Add New Reading")
        print("2. View All Readings")
        print("3. View Monthly Summary") 
        print("4. Exit") 
        choice = input("Enter your choice (1-4): ") 

        if choice == '1':
            add_reading_flow()
        elif choice == '2':
            display_all_readings()
        elif choice == '3': 
            display_monthly_summary_flow()
        elif choice == '4': 
            print("Exiting Blood Sugar Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


       
if __name__=="__main__":
    main()
