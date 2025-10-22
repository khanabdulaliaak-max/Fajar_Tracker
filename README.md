
Fajr Prayer Tracker - Streamlit App
===================================

Files:
- fajr_tracker.py    : The Streamlit web app
- requirements.txt   : Python packages needed
- README.md          : This file

How to run:
1. Make sure you have Python 3.8+ installed.
2. (Optional but recommended) Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # mac/linux
   venv\Scripts\activate   # windows
3. Install requirements:
   pip install -r requirements.txt
4. Run the app:
   streamlit run fajr_tracker.py

The app will open in your browser at http://localhost:8501 by default.

Notes:
- Data is stored locally in fajr_data.json in the same folder.
- The app automatically resets the stored data after 30 days from the start date.
- You can reset manually from the sidebar.
