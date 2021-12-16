# Picolo: A Smart Assistant

## Instruction guide for PicoloExtension
### Setup
1. Download the source code from https://github.com/TanviAgg/PicoloExtension. 
2. Chrome extension - Go to chrome: Manage Extensions -> Load unpacked. Upload the PicoloExtension directory which contains all the required files for the chrome extension. 
3. OCR server - Host a server using the following commands:
`export FLASK_ENV=development`;
`export FLASK_APP=basic_server.py`;
`flask run`
4. Now the server is ready (by default started on port 5000), and the chrome extension can be used to extract text from images. 

### How to use
1. Pin the extension to the toolbar and click on it. The screen will display a message saying “Capturing is Active”.
2. Select the bounding box for the area of interest using the cursor.
3. After the cursor is released, the converted text will be copied to the clipboard, for use as needed.

## Instruction guide for PicoloDesk
1. This project uses Python 3.8 and Tesseract 4.1.3. Download all other dependencies and set up the environment as per `requirements.txt`.
2. Execute the script main.py and it will display a pop-up with the screencapture.
3. Using the cursor select the part which you want to extract text from, and a green bounding box will appear. 
4. If you want to redo the selection, click the R key and go back to step 3.
5. Otherwise you can click on the C key, which will select the area and extract the text from it. Press any key to exit.


## Technical References
1. Screenshot capture on MAC - https://github.com/simov/screenshot-capture
2. Tesseract API for OCR - https://github.com/tesseract-ocr/tesseract
3. Copy text to clipboard in a chrome extension - https://stackoverflow.com/questions/3436102/copy-to-clipboard-in-chrome-extension
4. Tesseract Python API usage - https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
5. Tesseract usage - https://towardsdatascience.com/how-to-extract-text-from-images-using-tesseract-ocr-engine-and-python-22934125fdd5
6. REST API in python using Flask - https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
7. Enable cross-origin requests in Flask - https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
8. Plotting - https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

Copyright 2021: Tanvi Aggarwal