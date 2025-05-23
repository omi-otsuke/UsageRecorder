# UsageRecorder

## Overview

**UsageRecorder** is a tool designed to record server usage history.  
It allows users to input information such as start/end times, user name, connection account, purpose of use, target servers, and remarks, and saves the data to an Excel file.

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

### For user

1. Download the zip file from the link below:

   [Download UsageRecorder](https://github.com/omi-otsuke/UsageRecorder/releases/download/v1.0.0/UsageRecorder.zip)

2. Unzip the downloaded zip file. And place the downloaded folder in the appropriate location and place the shortcut file wherever you like, as needed.

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

```text
UsageRecorder/
├── source/
│   ├── ur.py                # Implementation of the UsageRecorder class
│   ├── ura.py               # Main code for the GUI application
│   ├── ure.py               # Definition of the UsageRecordEntity class
│   └── vld.py               # Validation logic
├── conf/
│   ├── system_conf.toml     # System configuration file
│   └── user_data.toml       # Template for user data
├── test/
│   └── test_ur.py           # Tests for the UsageRecorder class
├── README.md                # This file
├── .gitignore               # Specifies files to exclude from Git
└── requirements.txt         # Required Python libraries
```

---

## Configuration File

### `conf/system_conf.toml`

The configuration file includes the following settings:

```toml
output_file_path = "../output/usage_records.xlsx"  # Path to the output Excel file
sheet_name = "Sheet1"                              # Name of the Excel sheet
base_row = 4                                       # Starting row for data
purpose_choices = ["Purpose A", "Purpose B", "Purpose C"]  # Choices for purpose of use
destination_names = ["Server A", "Server B"]       # Target server names
```

### `conf/user_data.toml`

This file is used to store user-specific data, such as the user name, connection account, purpose of use, server names, and remarks. It serves as an example or template for user input. Below is an example structure:

```toml
user_name = "Example User"
connection_account = "example-account"
use_purpose = "Example Purpose"
server_names = ["Server A", "Server B", "Server C"]
remarks = "Example remarks"
```

You can edit this file to pre-fill the input fields in the application.

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
