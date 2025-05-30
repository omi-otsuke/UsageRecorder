# UsageRecorder

## Overview

**UsageRecorder** is a tool designed to record server usage history.  
It allows users to input information such as start/end times, user name, connection account, purpose of use, target servers, and remarks, and saves the data to an Excel file.  
In addition, after recording, executable files such as remote desktop can be automatically launched, allowing for a seamless transition from recording to actual work.

---

## Features

- **Record Start/End Times**: Logs the start and end times of server usage.
- **Validation**: Displays error messages if there are issues with the input data.
- **Save to Excel**: Saves the recorded data to a specified Excel file.
- **Configurable Settings**: Uses a TOML configuration file for customizable behavior.

---

## Requirements

- OS:
  - Windows 11 or higher
  - macOS 12 or higher
- Python 3.13 or higher
- Required Python libraries:
  - `wxPython`
  - `openpyxl`

---

## Installation

### Prerequisites

You will need to prepare the destination Excel file in advance. Excel samples in a format compatible with this tool are listed below, so please download them as needed and place them wherever you like:  
[automation_sample.xlsx](https://github.com/omi-otsuke/UsageRecorder/raw/refs/heads/master/output/automation_sample.xlsx)

### For user

1. Download the zip file from the link below:

   [Download UsageRecorder (zip)](https://github.com/omi-otsuke/UsageRecorder/releases/download/v1.0.0/UsageRecorder.zip)

2. Unzip the downloaded zip file. And place the unzipped folder in the appropriate location and place the shortcut file wherever you like, as needed.

3. Prepare the configuration file:

   - Edit `conf/system_conf.toml` and `conf/user_data.toml` as needed.

### For developer

1. Clone this repository:

   ```bash
   git clone https://github.com/omi-otsuke/UsageRecorder.git
   cd UsageRecorder
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Prepare the configuration file:

   - Edit `conf/system_conf.toml` and `conf/user_data.toml` as needed.

---

## Usage

1. Run the program:

   1. For user:
    Run the executable file (UsageRecorder.exe) or its shortcut.

   2. For developer:

   ```bash
   python source/ura.py
   ```

2. A GUI will appear. Enter the following information:
   - Start/End times
   - User name
   - Connection account
   - Purpose of use
   - Target servers
   - Remarks (optional)

3. After entering the data, click the "OK" button to save the data to the Excel file.

---

## Project Structure

```plain text
UsageRecorder/
├── source/
│   ├── ur.py                # Implementation of the UsageRecorder class
│   ├── ura.py               # Main code for the GUI application
│   ├── urcmn.py             # Definition of the common functions
│   ├── ure.py               # Definition of the UsageRecordEntity class
│   ├── urlog.py             # Definition of the logging related classes
│   └── vld.py               # Validation logic
├── conf/
│   ├── system_conf.toml     # System configuration file
│   └── user_data.toml       # Template for user data
├── log/
│   └── error.log            # Error log file
├── test/
│   └── test_ur.py           # Tests for the UsageRecorder class
├── requirements.txt         # Required Python libraries
├── build.bat                # Batch file for building on Windows
├── README.md                # This file
├── LICENSE                  # License declaration file
└── .gitignore               # Specifies files to exclude from Git
```

---

## Configuration File

### `conf/system_conf.toml`

The configuration file includes the following settings:

```toml
output_file_path = '\\server\directory\usage_records.xlsx' # Path to the output Excel file
sheet_name = "Sheet1"                              # Name of the Excel sheet
base_row = 4                                       # Starting row for data
log_file_path = "log/error.log"                    # Path to the log file
purpose_choices = ["Purpose A", "Purpose B", "Purpose C"] # Choices for purpose of use
destination_names = ["Server A", "Server B", "Server C"] # Target server names
application = 'C:\WINDOWS\system32\mstsc.exe'      # Executable path after the program has finished
arguments = ["mstsc", 'C:\Users\your-name\Desktop\example.rdp'] # Arguments to the executable
```

### `conf/user_data.toml`

This file is used to store user-specific data, such as the user name, connection account, purpose of use, server names, and remarks. You can edit this file to pre-fill the input fields in the application.
Below is an example structure:

```toml
user_name = "Example User"
connection_account = "example-account"
use_purpose = "Example Purpose"
server_names = ["Server A", "Server C"]
remarks = "Example remarks"
```

---

## Testing

You can run tests using `pytest`:

```bash
pytest test/
```

---

## Notes

- Ensure that the paths and settings in `conf/system_conf.toml` are correct.
- Be cautious not to expose private information (e.g., usernames, passwords) when sharing this project.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Feel free to open an issue for bug reports or feature requests. Pull requests are also welcome!
