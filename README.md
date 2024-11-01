# O.R.I.O.N: Your Voice-Controlled Assistant

This project is a voice-controlled assistant named O.R.I.O.N that can perform various tasks, including:

*   Opening websites in a web browser.
*   Logging into different services like LMS and Codetantra.
*   Checking and reconnecting to Wi-Fi.

## How it Works

The project uses the following libraries:

*   `speech_recognition`: For converting voice commands to text.
*   `pyttsx3`: For text-to-speech conversion.
*   `selenium`: For web automation (logging into websites).
*   `psutil`: For checking network connectivity.
*   `requests`: For making HTTP requests to check internet connectivity.
*   `mysql.connector`: For interacting with the MySQL database.
*   `dotenv`: For loading environment variables from a .env file.

The assistant works by listening for voice commands, processing them, and performing the corresponding actions. It uses regular expressions to identify the task and target from the voice command. For login tasks, it interacts with a MySQL database to retrieve user credentials.

## Setup and Usage

1.  Clone the repository: `git clone https://github.com/your-username/Assistant-ORION.git`
2.  Install the required packages: `pip install -r requirements.txt`
3.  Create a `.env` file and add your database credentials, Wi-Fi credentials, and Edge driver path:

```bash
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
WIFI_USERNAME=your_wifi_username
WIFI_PASSWORD=your_wifi_password
DRIVER_PATH=your_driver_path
```
## Run the main.py script: python main.py

## Speak your command when prompted, for example:

*	"Open YouTube"
*   "Login LMS"
*   "Login Codetantra"

# Project Structure

* `main.py`: The main script that runs the voice assistant.
* `data.py`: Handles database interactions for storing and retrieving user credentials.
* `login_setter.py`: Contains functions for logging into different websites.
* `checkwifi.py`: Checks for internet connectivity and reconnects to Wi-Fi if needed.
* `siteopener.py`: Fetches website URLs from the database and opens them in a browser.
* `README.md`: This file.

