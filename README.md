ADVANCED BLOOD BANK MANAGEMENT SYSTEM


The Advanced Blood Bank Management System is a desktop application built with Python's tkinter for managing blood donor information. It allows users to register donors, track donation history, search for donors, and ensure donor eligibility. The data is stored persistently using SQLite.

FEATURES

   1.Donor Registration
              Add donors with details such as name, age, blood group, contact, and last donation date.
              Check donor eligibility based on a 90-day donation interval.
  
   2.Donation History Tracking
              Automatically records donation dates for registered donors.

   3.Search Donors
             Search by blood group or donor name.
             
   4.Display and Manage Donors
             View all registered donors in a tabular format.
             Editable donor details (optional functionality can be added).
   5.Data Persistence
             Donor data and donation history are stored in an SQLite database.


Technologies Used
Programming Language: Python
GUI Framework: tkinter
Database: SQLite

Installation and Setup
Prerequisites
Python 3.x installed on your system.
Required Python libraries:
tkinter (comes pre-installed with Python)
sqlite3 (comes pre-installed with Python)

Steps to Run
Clone or download the repository.
Ensure Python 3.x is installed on your system.
Run the following command to execute the application:
bash
Copy code
python advanced_blood_bank.py
How to Use
Add Donor

Fill in the donor details in the form and click "Add Donor".
Ensure the Last Donation Date (if provided) is in YYYY-MM-DD format.
Search Donors

Use the search section to find donors by blood group or name.
Select the appropriate search option (Blood Group or Name) and enter the value.
View Donation History
