import pytest
import os
from datetime import datetime
import csv 


from project import (
    get_state,
    load_data,
    save_new_reading,
    get_monthly_summary_data,
    DATA_FILE,
    HEADERS
)

# --- Fixture for cleaning up the data file between tests ---
@pytest.fixture(autouse=True)
def clean_data_file():
    """Ensures a clean data.csv file before and after each test."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield 
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

# --- Test Function 1: Thoroughly Test get_state() ---
def test_get_state_classification():
    """
    Tests the get_state function for correct classification across different ranges.
    """
    assert get_state(50) == "Low", "Should classify 50 as Low"
    assert get_state(69) == "Low", "Should classify 69 (just below min) as Low"
    assert get_state(0) == "Low", "Should classify 0 as Low" 

    assert get_state(70) == "Normal", "Should classify 70 (min) as Normal"
    assert get_state(100) == "Normal", "Should classify 100 as Normal"
    assert get_state(139) == "Normal", "Should classify 139 (max) as Normal"

    assert get_state(140) == "High", "Should classify 140 (just above max) as High"
    assert get_state(250) == "High", "Should classify 250 as High"
    assert get_state(500) == "High", "Should classify 500 as High" # Another edge case


# --- Test Function 2: Test Data Persistence (Save & Load) ---
def test_data_persistence():
    """
    Tests if data can be correctly saved to the CSV and then loaded back,
    ensuring data integrity for multiple entries and empty file handling.
    """
    # Test loading from an initially empty file
    assert load_data() == [], "load_data should return empty list for empty/non-existent file"

    # Define test data
    timestamp1 = datetime(2025, 1, 1, 10, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    blood_sugar1 = 95.0
    state1 = "Normal"

    timestamp2 = datetime(2025, 1, 2, 14, 30, 0).strftime("%Y-%m-%d %H:%M:%S")
    blood_sugar2 = 180.0
    state2 = "High"

    # Save the first reading
    save_new_reading(blood_sugar1, state1, timestamp1)
    
    # Load and verify the first reading
    loaded_data_1 = load_data()
    assert len(loaded_data_1) == 1, "Should load 1 row after first save"
    assert loaded_data_1[0] == [timestamp1, blood_sugar1, state1], "First saved data should match"

    # Save the second reading
    save_new_reading(blood_sugar2, state2, timestamp2)

    # Load and verify both readings
    loaded_data_2 = load_data()
    assert len(loaded_data_2) == 2, "Should load 2 rows after second save"
    assert loaded_data_2[0] == [timestamp1, blood_sugar1, state1], "First data should still be correct"
    assert loaded_data_2[1] == [timestamp2, blood_sugar2, state2], "Second saved data should match"

    # Ensure header is written only once (implicitly tested by loading after multiple saves)
    with open(DATA_FILE, 'r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)
        assert lines[0] == HEADERS, "Header should be written and correct"
        assert len(lines) == 3, "CSV file should have 1 header row + 2 data rows"


# --- Test Function 3: Test Monthly Summary Calculations ---
def test_monthly_summary_calculations():
    """
    Tests the get_monthly_summary_data function for accurate calculations
    of average, min, max, and state counts across a specific month,
    handling data from other months.
    """
    # 1. Prepare test data spanning multiple months/years
    test_data = [
        # January 2025 data
        {"ts": datetime(2025, 1, 5, 8, 0, 0), "bs": 90.0, "state": "Normal"},
        {"ts": datetime(2025, 1, 10, 12, 0, 0), "bs": 150.0, "state": "High"},
        {"ts": datetime(2025, 1, 15, 18, 0, 0), "bs": 65.0, "state": "Low"},
        {"ts": datetime(2025, 1, 20, 9, 0, 0), "bs": 110.0, "state": "Normal"},
        {"ts": datetime(2025, 1, 25, 7, 0, 0), "bs": 140.0, "state": "High"},
        
        # February 2025 data (should be ignored for Jan summary)
        {"ts": datetime(2025, 2, 1, 10, 0, 0), "bs": 120.0, "state": "Normal"},
        
        # December 2024 data (should be ignored for Jan summary)
        {"ts": datetime(2024, 12, 1, 10, 0, 0), "bs": 80.0, "state": "Normal"},
    ]

    # Save all test data to the CSV file
    for item in test_data:
        save_new_reading(item["bs"], item["state"], item["ts"].strftime("%Y-%m-%d %H:%M:%S"))

    # 2. Call the function to be tested for January 2025
    summary = get_monthly_summary_data(2025, 1)

    # 3. Assert the results
    assert summary is not None, "Summary should not be None for January 2025 data"
    assert summary["total_readings"] == 5, "Should count 5 readings for January 2025"
    
    # Calculate expected values manually for verification
    expected_readings_jan = [90.0, 150.0, 65.0, 110.0, 140.0]
    
    # Check average (using pytest.approx for float comparisons)
    assert summary["avg"] == pytest.approx(sum(expected_readings_jan) / len(expected_readings_jan)), "Average should be correct"
    
    # Check min and max
    assert summary["min"] == min(expected_readings_jan), "Min should be correct"
    assert summary["max"] == max(expected_readings_jan), "Max should be correct"

    # Check state counts
    assert summary["normal_count"] == 2, "Should have 2 normal readings"
    assert summary["low_count"] == 1, "Should have 1 low reading"
    assert summary["high_count"] == 2, "Should have 2 high readings"

# --- Additional Test  ---
def test_monthly_summary_no_data():
    """
    Tests get_monthly_summary_data when there is no data for the requested month.
    """
    # Save some data, but not for the month we'll query
    save_new_reading(100.0, "Normal", datetime(2025, 1, 1).strftime("%Y-%m-%d %H:%M:%S"))
    save_new_reading(120.0, "Normal", datetime(2025, 1, 2).strftime("%Y-%m-%d %H:%M:%S"))

    # Query for a month with no data
    summary = get_monthly_summary_data(2025, 2)
    assert summary is None, "Summary should be None when no data for the month"
