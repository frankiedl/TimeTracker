# Time Tracker

A simple yet powerful desktop application for tracking time spent on projects and calculating billable amounts. Built with Python and Tkinter, this application supports multiple currencies and provides a user-friendly interface for time tracking and project management.

![image](https://github.com/user-attachments/assets/298bf7b7-b149-49c0-8bba-55611b8fd79d)


## Features

- **Real-time Time Tracking**: Start and stop timer for tracking work sessions
- **Project Management**: Create and manage multiple projects
- **Rate Management**: Set different rates for different projects
- **Multi-currency Support**: 
  - Euro (€)
  - US Dollar ($)
  - British Pound (£)
  - Japanese Yen (¥)
  - Chinese Yuan (元)
- **Automatic Calculations**: 
  - Total time per project
  - Billable amount based on rate and time
- **Data Persistence**: All data is stored in Excel format
- **Clean Interface**: Modern, intuitive user interface
- **Session History**: Keeps track of all work sessions

## Requirements

- Python 3.6 or higher
- Required Python packages (automatically installed on first run):
  - pandas
  - openpyxl
  - tkinter (usually comes with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/frankiedl/TimeTracker.git
cd time-tracker
```

2. Run the application using one of these methods:

### Windows
Double click on `time-tracker.bat` or run it from the command line:
```bash
time-tracker.bat
```
The batch file will:
- Check if required packages (pandas and openpyxl) are installed
- Install missing packages automatically
- Launch the Time Tracker application

### Other Operating Systems
Install required packages and run the Python script directly:
```bash
pip install pandas openpyxl
python time_tracker.py
```

## Usage

### Starting a New Project

1. Launch the application using `time-tracker.bat` or `python time_tracker.py`
2. Click the '+' button next to the Project dropdown
3. Enter the project name when prompted
4. Click OK to create the project

### Setting Up Rates

1. Click the '+' button next to the Rate dropdown
2. Enter the rate for 8 hours of work
3. Select the desired currency from the Currency dropdown
4. The rate will be automatically converted to a per-minute rate for calculations

### Tracking Time

1. Select a project from the dropdown
2. Select a rate from the rate dropdown
3. Click the START button to begin tracking
4. Click the STOP button when finished
5. The total time and billable amount will be automatically updated

### Viewing Project Totals

- Total project time and billable amount are displayed at the bottom of the application
- These totals are automatically updated when switching between projects or after tracking sessions

## Project Structure

```
time-tracker/
│
├── time_tracker.py     # Main application script
├── time-tracker.bat    # Windows batch file for easy execution
├── time_tracking.xlsx  # Data storage file (created on first run)
├── README.md          # This documentation
└── screenshots/       # Application screenshots
```

## Data Storage

All data is stored in an Excel file (`time_tracking.xlsx`) with the following columns:
- Project
- Date
- Start_Time
- End_Time
- Duration_Minutes
- Rate
- Currency

## Features in Development

- Currency conversion support
- Data export functionality
- Detailed reporting
- Multi-language support
- Dark mode theme

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and Tkinter
- Uses Pandas for data management
- Modern UI design inspired by Material Design principles

## Support

If you encounter any problems or have suggestions, please open an issue in the GitHub repository.

## Screenshots

### Main Interface
![image](https://github.com/user-attachments/assets/e9bd4f8b-d8d1-4700-8b93-63067b39c3a0)


### Adding a New Project
![image](https://github.com/user-attachments/assets/aba36b81-12df-4640-9dab-7b968600c94e)


### Setting Rates
![image](https://github.com/user-attachments/assets/205b2998-4331-45b5-a4b9-3489faecdd15)


## Batch File Details

The included `time-tracker.bat` file provides the following functionality:

1. Changes to the directory where the script is located
2. Checks if pandas is installed, installs it if missing
3. Checks if openpyxl is installed, installs it if missing
4. Launches the Time Tracker application

This makes the application easy to run on Windows systems without manually installing dependencies or running Python commands.


# Changelog Time Tracker v1.2.1

## Bug Fixes
- Fixed indentation of `setup_ui` method to be properly inside the `TimeTrackerApp` class
- Added debug print in `check_activity` to track inactivity detection

## Changes
- Reduced inactivity threshold from 10 minutes to 5 minutes (300 seconds)
- Changed inactivity check interval to run every second
- Added immediate activity checking on tracking start

## Previous Changes (v1.2.0)
- Added multi-currency support
- English UI
- Automatic dependency installation
- Excel-based data storage with proper data types
- Project and rate management

## Technical Updates
- DataFrame handling improvements
- Activity detection optimization
- UI responsiveness improvements

## Notes
- Functionality requires Windows for inactivity detection
- Excel file is created on first run
- All times are saved in local timezone

To test inactivity detection:
1. Start tracking a project
2. Do not move mouse or use keyboard
3. The app should stop after 5 minutes of inactivity
