# CS 1520 Final Project by Joshua Hellauer -- McDonalds website / kiosk ordering system

## Purpose:

- Offer an interface for customers to place their orders which are received by the kitchen by using an sqlite database.

# Requirements:

- Python 3.12.0

# Installation:

- **1.)** Download and unzip the compressed project folder to your desired location.
- **2.)** Navigate to the root of the project directory
- **3).** Create a python virtual environment.
- **4).** Ensure the virtual environment has been activated `venv\Scripts\activate`
- **5).** Install all dependencies using `pip install -r requirements.txt`
- **6).** Run the main app using `python main_app.py`, keep this terminal open while using
- **7).** Navigate to the link given, eg `http://127.0.0.1:5000`

# Usage:

Main page:

- Navigate through different food categories with the left navigation bar
- Use the plus and minus buttons to change desired quantity of a product, then click `Add to order` for it to be added to your order summary
- Click on product images to view more information
- When finished, enter your name and click `Place Order` to submit your order to the kitchen
- You will be able to view your order for ten seconds before the app reroutes to the main page

Kitchen:

- To view the kitchen, click `View the kitchen ->`, or navigate to `<root-directory>/kitchen`
- Delete orders from the database by clicking `Print / complete`
- Naviagate back to the kiosk page with the link in the upper left corner
- This page refreshes every 15 seconds, so no need to manually refresh.
