# GlucoTrack 🩺

> A Python CLI application for blood glucose monitoring and health insights

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![CS50P](https://img.shields.io/badge/CS50P-Final%20Project-red.svg)](https://cs50.harvard.edu/python/)

## Overview

GlucoTrack helps individuals monitor and analyze their blood glucose levels through an intuitive command-line interface. Built with reliability in mind, it provides real-time classification, historical tracking, and meaningful health insights to support diabetes management and wellness monitoring.

**🎥 [Demo Video](https://youtu.be/y1Gnm2NCfpo)**

## Key Features

- **🔍 Smart Classification** - Automatically categorizes readings as Low, Normal, or High
- **📊 Historical Tracking** - Clean, tabulated view of all past readings  
- **📈 Monthly Reports** - Statistical summaries with health insights
- **🛡️ Robust Error Handling** - Graceful handling of invalid inputs and data issues
- **💾 Persistent Storage** - CSV-based data storage for cross-session reliability

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jaaferbenahmed/glucotrack.git
cd glucotrack

# Install dependencies
pip install tabulate

# Run the application
python project.py

# Run tests
pip install pytest
pytest test_project.py -v
```

## Usage

### Main Menu Options

1. **Add New Reading** - Input glucose level with automatic timestamp
2. **View All Readings** - Display complete history in table format
3. **Monthly Summary** - Generate detailed reports for specific months
4. **Exit** - Save and close application

### Example Workflow

```
--- Blood Sugar Tracker Menu ---
1. Add New Reading
2. View All Readings  
3. View Monthly Summary
4. Exit
Enter your choice (1-4): 1

Enter your blood sugar level (mg/dL): 95
Reading: 95.0 mg/dL, State: Normal, Time: 2025-01-15 10:30:45
Reading successfully saved.
```

## Architecture & Design

### Core Components

- **`project.py`** - Main application with user flows and business logic
- **`test_project.py`** - Comprehensive test suite with pytest
- **`data.csv`** - Local data storage (auto-generated)

### Key Design Decisions

**CSV vs JSON Storage:** Chose CSV for its simplicity, Excel compatibility, and lightweight structure perfect for tabular health data.

**Modular Architecture:** Separated concerns into focused functions (`get_state`, `load_data`, `get_monthly_summary_data`) for testability and maintainability.

**Graceful Error Handling:** App continues running despite invalid inputs or file issues, with clear user feedback.

**Health-Focused UX:** Simple prompts, clear classifications, and actionable health insights prioritize user experience.

## Testing

Comprehensive test coverage includes:
- ✅ State classification accuracy across all ranges
- ✅ Data persistence and integrity 
- ✅ Monthly summary calculations
- ✅ Edge case handling (empty files, malformed data)

```bash
pytest test_project.py -v
# Expected: All tests pass with detailed output
```

## Health Guidelines

**Reference Ranges Used:**
- **Normal:** 70-139 mg/dL
- **Low:** < 70 mg/dL  
- **High:** > 139 mg/dL

*Note: This tool is for tracking purposes only. Always consult healthcare professionals for medical decisions.*

## Contributing

Feedback and contributions welcome! Whether you spot bugs, have feature ideas, or want to improve the code:

1. Open an issue for discussion
2. Fork the repository  
3. Create a feature branch
4. Submit a pull request

## Future Enhancements

- 📱 GUI interface with tkinter/PyQt
- 📤 Export reports to PDF/Excel
- 🔔 Configurable health alerts
- 📊 Trend visualization with matplotlib
- ☁️ Cloud sync capabilities

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ as part of CS50's Introduction to Programming with Python**
**📜 [View Certificate](https://certificates.cs50.io/e5b9c705-4b4a-41ea-88ea-6bc22fbb6957.pdf?size=letter)**

*"Good code isn't just about syntax - it's about solving real problems for real people."*
