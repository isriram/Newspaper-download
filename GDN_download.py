from BeautifulSoup import BeautifulSoup as Soup
from pyPdf import PdfFileWriter, PdfFileReader
from datetime import datetime
import urllib
import re,os

def downloadPage(url):
    pageData = urllib.urlopen(url).read()
    return pageData

def pageSectionStrip(pageData, markerTop, markerBottom ):    
    locTop = pageData.find(markerTop)
    locBottom = pageData.find(markerBottom)
    sectionText = pageData[locTop:locBottom]
    return sectionText

def scrapeData(sectionText):
    arrangedPage = Soup(''.join(sectionText))
    extractedLinks = arrangedPage.findAll('a')
    return extractedLinks

def regexLinks(extractedLinks):
    site = "http://www.gulf-daily-news.com/"
    re1='.*?'   # Non-greedy match on filler
    re2='(".*?")'   # Double Quote String 1

    rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
    rgx=[]
    l = len(extractedLinks)
        
    for i in range(0,l):
        tmpVar = str(extractedLinks[i])
        m = rg.search(str(extractedLinks[i]))
        if m:
             if ".pdf" in m.group(1):
                 rgx = rgx + [site + m.group(1)]

    l = len(rgx)
    for i in range(0,l):
        rgx[i] = rgx[i].replace('"','')

    return rgx

def downloadData(linkPaths):
    if "<type 'list'>" != str(type(linkPaths)):
        print "Invalid parameter passed.\n"
        return
    l = len(linkPaths)

    for i in range(0,l):
        print "Downloading page " + str(i+1) + " of " + str(l)
        Page = urllib.urlopen(linkPaths[i]).read()
        F = open("./Tmp/" + str(i+1) + ".pdf", "wb")
        print "Writing page " + str(i+1) + " of " + str(l)
        F.write(Page)
        F.close()

    return

def writePDF(linkPaths):
    if "<type 'list'>" != str(type(linkPaths)):
        print "Invalid parameter passed.\n"
        return

    l = len(linkPaths)

    output = PdfFileWriter()
    for i in range(0,l):
        input1 = PdfFileReader(file("./Tmp/" + str(i+1) + ".pdf", "rb"))
        output.addPage(input1.getPage(0))
     
    print("Generating newspaper...\n")
    dateObject = datetime.now()
    fileName = dateObject.strftime("%Y%m%d")

    fileName = "GDN " + fileName + ".pdf"

    outputStream = file(fileName, "wb")
    output.write(outputStream)
    outputStream.close()

    return
    
def main():
    url = "http://www.gulf-daily-news.com/digital.aspx"
    site = "http://www.gulf-daily-news.com/"
    urlList = []

    markerTop = ("<!-----------START MAINCONTENT ------------>")
    markerBottom = ("<!-- AddThis Button END -->")

    pgData = downloadPage(url)
    dataText = pageSectionStrip(pgData, markerTop, markerBottom)
    extractedLinks = scrapeData(dataText)
    pageURL = regexLinks(extractedLinks)
    downloadData(pageURL)
    writePDF(pageURL)
    return

main()
