
# Server Computer code support for ESP32 App KLTN COMPUTER LAB MANAGEMENT APP


## Usage File

Step 1: Please fill in these two pieces of information
```python
FIREBASE_HOST = "Link to your Realtime Database"
CRED_PATH = "Path to your Firebase .json file"
```
Step 2: Compile the code into an .exe file and install it on your computer Command to package the code into an .exe file:
```python
pyinstaller --onefile --add-data "Path to your firebase.json file;." NameOfYourPythonScript.py

```
