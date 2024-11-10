# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.lib import colors

# initializing variables with values
fileName = 'call_report.pdf'
x = ['hello', 'hi', 'your mom fuddi']
documentTitle = 'Call_Summary'
title = 'CALL SUMMARY'
subTitle = '.....Summary of the customer support call......'
textLines = x
# image = 'Logo(4).png'

# creating a pdf object
pdf = canvas.Canvas(fileName)

# setting the title of the document
pdf.setTitle(documentTitle)

# Using a standard font for the title
pdf.setFont('Helvetica-Bold', 36)  # Changed font to Helvetica-Bold
pdf.drawCentredString(300, 770, title)

pdf.setFillColorRGB(0, 0, 255)
pdf.setFont("Courier-Bold", 12)
pdf.drawCentredString(290, 740, subTitle)

# drawing a line
pdf.line(30, 720, 550, 720)

# Setting text for content with another standard font
text = pdf.beginText(40, 680)
text.setFont("Courier", 16)
text.setFillColor(colors.black)
for line in textLines:
    text.textLine(line)
pdf.drawText(text)

pdf.save()
