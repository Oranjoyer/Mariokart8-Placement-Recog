# Mariokart8-Placement-Recog
Project to identify and output what placement a player is in based on image data and templates (Splitscreen not currently supported)

Use flaskApp.py to test, manage page is at localhost:8000/manage

Base Placements and Usernames
localhost:8000

You can select a specific piece with
localhost:8000/<Camera Index>/<name or place (omit for both)>

Use fullscreen (No Nintendo Switch Overscan Scaling) video capture of Mario Kart Gameplay before a race starts and see the magic unfold

use getTemplates.py with collection of labeled images to create templates (No need to with the preset templates)

Dependencies:
Python
Numpy
OpenCV
Flask
