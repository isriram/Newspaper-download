from pyPdf import PdfFileWriter, PdfFileReader
from datetime import datetime
import urllib

def main():
	dateObject = datetime.now()
	fileName = dateObject.strftime("%Y%m%d")
	
	fileName = "Daily Tribune " + fileName + ".pdf"
	
	url = "http://www.dt.bh/DigitialPDF/DailyTribune_Epaper.pdf"
	page = urllib.urlopen(url)
	print("Downloading todays' newspaper...\n")
	newsPaper = page.read()
	
	print("Writing file " + str(fileName) + "\n")
	f = open(fileName, "wb")
	f.write(newsPaper)
	f.close()
	return

main()
