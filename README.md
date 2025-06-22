# Title Tracker

Author: Zain <zain@hillthrillmotoplex.com>


## Setup

1. Install Python 3.7+.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Import Data

To import your existing Excel data:
```bash
python import_excel.py "Titles coming in.xlsx"
```

## Import from Google Sheets

To import directly from your Google Sheet, run:
```bash
python import_sheet.py "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0"
```
This will fetch the sheet as CSV and import into the database.

## Run the App

```bash
python app.py
```

## Create Executable (Windows)

Install PyInstaller:
```bash
pip install pyinstaller
```
Then package:
```bash
pyinstaller --onefile app.py
```
The executable will be in `dist/app.exe`.
