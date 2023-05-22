import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
from fpdf import FPDF



# creating a pdf file object
pdfFileObj = open('schedule.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# extracting text from page
text = ''
for page in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(page)
    text += (pageObj.extractText())


# Patterns for finding the time schedules in the text for AM and PM
pattern1  = re.compile(r'(\d?\d[:]\d\d)(\s*)([PM]{2})')
pattern2  = re.compile(r'(\d?\d[:]\d\d)(\s*)([AM]{2})')
pattern3  = re.compile(r'\b(\d)([:]\d\d)')



time = pattern3.finditer(text)

# These statements will substitute the time with the AM and PM, thus removing the AM and PM from the text
subbed_time1 = pattern2.sub(r'\1', text)
subbed_time2 = pattern1.sub(r'\1', subbed_time1)
subbed_time3 = pattern3.sub(r'\1', subbed_time2)

split_on = "12:30"
half_txt = subbed_time2.split(split_on, 2)

# The converted and uncoverted lists are used for finding and replacing the 12 hours time 
# with 24 hour time format
unconverted = []
converted = []
    
for t in time:
    converted.append(str(int(t.group(1))+12)+str(t.group(2)))
    unconverted.append(str(t.group(0)))

subbed_time2 = str(subbed_time2)

txt = str(half_txt[2])
for (u, c) in zip(unconverted, converted):
    txt = txt.replace(u, c)
    
txt = half_txt[0] + split_on + half_txt[1] + split_on +  txt

pattern4 = re.compile(r'(\d\d\d[:]\d\d)')
txt = pattern4.sub("14:00", txt)

print(txt)

file1 = open('myText.txt', 'w+')

file1.write(txt)



pdfFileObj.close()


# save FPDF() class into 
# a variable pdf
pdf = FPDF()   
   
# Add a page
pdf.add_page()
   
# set style and size of font 
# that you want in the pdf
pdf.set_font("Arial", size = 15)
  
# open the text file in read mode
f = open("myText.txt", 'r')
  
# insert the texts in pdf
for x in f:
    pdf.cell(200, 10, txt = x, ln = x, align = 'C')
   
# save the pdf with name .pdf
pdf.output("new-schedule.pdf")   