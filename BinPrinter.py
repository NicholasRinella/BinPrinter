# BinPrinter.py
# 2022-07-04
# Ver 1.0.2

#Import libraries
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import os, math, fnmatch, time
from pathlib import Path
from typing import Iterable, Any, Tuple

#Define functions
def signal_last(it:Iterable[Any]) -> Iterable[Tuple[bool, Any]]:    #Determines the last iterable
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var

def saveBitSheet(bitsheet, sheetNumber):
    bitsheet.save('./output/binsheet' + str(sheetNumber) + '.png')  #Save the bitsheet image to directory
    print('Saving binsheet' + str(sheetNumber) + ' to /output directory')   #Print info to console

def decorateBitSheet(bitsheet, fsize, fname, pageNumber, bitSize):
    bitsheet = bitsheet.resize((imageWidth, imageHeight), resample=0)                                           #Resize bitsheet to printable resolution
    draw = ImageDraw.Draw(bitsheet)                                                                             #Convert bitsheet to drawable
    font = ImageFont.truetype('RobotoMono-Regular.ttf', 50)                                                     #Initialize Font

    fnameText = fname
    fsizeText = str(round(fsize/1024, 2)) + 'KB'
    pageNumberText = str(pageNumber)

    fnameWidth, fnameHeight = draw.textsize(fname, font=font)                                                   #Get width and height of fname
    fsizeWidth, fsizeHeight = draw.textsize(fsizeText, font=font)                                              #Get width and height of fsize
    pageNumberWidth, pageNumberHeight = draw.textsize(str(pageNumber), font=font)                               #Get width and height of pageNumber
    draw.text(((bitsheet.width-fnameWidth)/2, (bitsheet.height-85)), fname, fill='black', font=font)                     #Draw fname
    draw.text((85, bitsheet.height-85), fsizeText, fill='black', font=font)                                    #Draw fsize
    draw.text(((bitsheet.width-pageNumberWidth)-85, bitsheet.height-85), str(pageNumber), fill='black', font=font)                 #Draw page number

    return(bitsheet)                                                                                            #Return the 'decorated' bitsheet

def newBitSheet():
    sheet = Image.new('RGB', (sheetWidth, sheetHeight), (255, 255, 255)) #Create a bitsheet
    #Draw edge marker around bitsheet
    for xx in range(sheetWidth):    #Horizontal edge markers
        sheet.putpixel((xx, 0), (0, 0, 0, 255))
        sheet.putpixel((xx, sheetHeight-1), (0, 0, 0, 255))
    for yy in range(sheetHeight):   #Vertical edge markers
        sheet.putpixel((0, yy), (0, 0, 0, 255))
        sheet.putpixel((sheetWidth-1, yy), (0, 0, 0, 255))
    return(sheet) #Return the newly created bitsheet


#Title
print('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n██░▄▄▀██▄██░▄▄▀██░▄▄░█░▄▄▀██▄██░▄▄▀█▄░▄█░▄▄█░▄▄▀██\n██░▄▄▀██░▄█░██░██░▀▀░█░▀▀▄██░▄█░██░██░██░▄▄█░▀▀▄██\n██░▀▀░█▄▄▄█▄██▄██░████▄█▄▄█▄▄▄█▄██▄██▄██▄▄▄█▄█▄▄██\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀')
#Program info
print('github.com/SyntaxBreak/BinPrinter')
print('Ver 1.0.1')
print('\n')

#Print instructions
print('Instructions:\nW --- WRITE data to BinSheets\nR --- READ data from BinSheets\nQ --- QUIT the program')
print('\n')


#Begin program
endProgram = False
while endProgram == False:

    #Get input
    command = input('>')


    #-------------------- Write Command -------------------- 
    if command == 'w' or command == 'W':

        #Check for output directory
        if os.path.exists('./output') == False:
            os.mkdir('./output')    #Make output directory if it doesnt exist

        #Get file data
        dataValid = False
        while dataValid == False:
            filePath = input('Enter file path:')    #Get path of file to encode
            try:
                file = open(filePath, 'rb')         #Open file
                dataValid = True
            except:
                print('File does not exist at given directory!\n')

        if dataValid == True:
            data = file.read()                      #Read binary from file

        #Initialize OutputBinSheet variables
        imageWidth = 2550
        imageHeight = 3300
        bitSize = 10            #width/height of one bit in pixels

        #Initialize BinSheet variables
        edgeMarkerWidth = 1                                             #Thickness of the line running around the edge of the bitsheet, used to indicate the bounds of the bitsheet
        sheetWidth = int((imageWidth/bitSize) - edgeMarkerWidth)        #Width of binsheet in pixels (1 pixel per bit)
        sheetHeight = int((imageHeight/bitSize) - edgeMarkerWidth)      #Height of binsheet in pixels (1 pixel per bit)
        rowCount = math.floor(sheetHeight/8) - 1                        #Number of rows per BinSheet (a row is 8 bits tall)
        sheet = newBitSheet()                                           #Make a new BinSheet

        #Write binary to the bitsheet
        page = 0
        row = 0
        xx = edgeMarkerWidth

        for is_last_element, byte in signal_last(data):
            byteString = ''
            bit = 1
            yy = 0
            while bit <= 128: #Loop through bits of each byte
                if byte&bit != 0:
                    sheet.putpixel((xx, yy + (row*8) + edgeMarkerWidth), (0, 0, 0, 255))          #Draw 1 bit to bitsheet
                    byteString += '1'
                else:
                    sheet.putpixel((xx, yy + (row*8) + edgeMarkerWidth), (255, 255, 255, 255))    #Draw 0 bit to bitsheet
                    byteString += '0'
                bit *= 2
                yy += 1
            xx += 1
            #print(byteString)

            if xx == sheetWidth-(edgeMarkerWidth): #Row is full
                #Move to next row
                row += 1
                xx = edgeMarkerWidth

            if row >= rowCount: #Page is full
                bitsheetFinished = decorateBitSheet(sheet, os.path.getsize(filePath), os.path.basename(filePath), page, bitSize) #Add finishing touches to the bitsheet
                saveBitSheet(bitsheetFinished, page) #Save bitsheet to output directory

                page += 1   #Move to next page
                row = 0     #Reset row counter

                sheet = newBitSheet()   #Create new bitsheet

            if is_last_element:
                bitsheetFinished = decorateBitSheet(sheet, os.path.getsize(filePath), os.path.basename(filePath), page, bitSize) #Add finishing touches to the bitsheet
                saveBitSheet(bitsheetFinished, page) #Save bitsheet to output directory
        

        print('Done!')
        time.sleep(1)


    #-------------------- Read Command -------------------- 
    elif command == 'r' or command == 'R':
        def point_direction(p1, p2):
            xDelta = p1[0]-p2[0]
            yDelta = p1[1]-p2[1]
            angle = math.atan(yDelta/xDelta)
            return(angle)

        def bitsheet_straighten(scan):
            
            #Find top edge marker
            for i in range(scan.height):
                position = (int(scan.width/2), i)
                if scan.getpixel(position) < (120):
                    topEdge = i
                    break
                
            originX = int(scan.width/2)
            originY = topEdge
            
            #Find coords of top left corner
            topLeftX = 0
            topLeftY = 0
            for topLeftX in range(int(scan.width/2)):
                #If the top pixel is black
                if scan.getpixel((originX-topLeftX, originY+topLeftY-1)) < 120:
                    topLeftY -= 1   #Move up
                #If the bottom pixel is white
                if scan.getpixel((originX-topLeftX, originY+topLeftY)) > 120:
                    topLeftY += 1   #Move down

                #If next step is too steep
                if scan.getpixel((originX-topLeftX, originY+topLeftY+2)) > 120:
                    break #We've reached the end of the top edge
            topLeftPos = (originX-topLeftX, originY+topLeftY)
            
            #Find coords of top right corner
            topRightX = 0
            topRightY = 0
            for topRightX in range(int(scan.width/2)):
                #If the top pixel is black
                if scan.getpixel((originX+topRightX, originY+topRightY-1)) < 120:
                    topRightY -= 1   #Move up
                #If the bottom pixel is white
                if scan.getpixel((originX+topRightX, originY+topRightY)) > 120:
                    topRightY += 1   #Move down

                #If next step is too steep
                if scan.getpixel((originX+topRightX, originY+topRightY+2)) > 120:
                    break #We've reached the end of the top edge
            topRightPos = (originX+topRightX, originY+topRightY)

            #Calculate angle delta to correct for
            rotationDelta = math.degrees(point_direction(topLeftPos, topRightPos))

            #AAAAANNNND FINALLY, correct for the rotation! :D
            output = scan.rotate(rotationDelta, fillcolor=255) #Rotate, and fill blank space with white
            return(output) #Output the straightened bitsheet

        #Find input directory
        try:
            os.mkdir('./input')
            print('No /input directory found!')
            print('Creating one...')
            print('Put binsheets into the input directory and try again')
        except:
            print('Found input directory')

            bitsheetCount = len(fnmatch.filter(os.listdir('./input'), '*.png'))

            #Are there any bitsheets?
            if bitsheetCount > 0:
                #Yes, carry on
                print('Found binsheets')

                #Order the bitsheets by timestamp
                paths = sorted(Path('./input').iterdir(), key=os.path.getmtime)
                print('Ordered binsheets by timestamp')

                #Initialize Image
                imageWidth = 2550
                imageHeight = 3300
                bitSize = 10            #width/height of one bit in pixels

                #Initialize BitSheet
                edgeMarkerWidth = 1     #Thickness of a line running around the edge of the bitsheet, used to indicate the bounds of the bitsheet
                sheetWidth = int((imageWidth/bitSize) - edgeMarkerWidth)
                sheetHeight = int((imageHeight/bitSize) - edgeMarkerWidth)
                rowCount = math.floor(sheetHeight/8) - 1

                output = open('OUTPUT.jpg', 'wb') #Open new binary file
                print('Beginning byte buffer')
                buffer = bytearray()
                bitsheetId = 0 #Initialize bitsheet id

                for bitsheetId in range(bitsheetCount): #Loop through bitsheets
                    sheet = Image.open(paths[bitsheetId])   #Open current bitsheet
                    sheet = sheet.convert("1")              #Make image black and white
                    sheet = bitsheet_straighten(sheet)       #Straighten the bitsheet

                    #crop image margins off
                    leftCrop = 0
                    while sheet.getpixel((leftCrop, sheet.height/2)) > (120):   #Left margin
                        leftCrop += 1
                    topCrop = 0
                    while sheet.getpixel((sheet.width/2, topCrop)) > (120):   #Top margin
                        topCrop += 1
                    rightCrop = 1
                    while sheet.getpixel(((sheet.width)-rightCrop, sheet.height/2)) > (120):   #Right margin
                        rightCrop += 1
                    bottomCrop = 1
                    while sheet.getpixel((sheet.width/2, (sheet.height)-bottomCrop)) > (120):   #Bottom margin
                        bottomCrop += 1
                    sheet = sheet.crop((leftCrop, topCrop, sheet.width-rightCrop, sheet.height-bottomCrop)) #Perform crop

                    sheet = sheet.resize((sheetWidth, sheetHeight), resample=0) #Crush image back down so one bit is 1 pixel
                    
                    #Decode the bitsheet
                    for row in range(rowCount): #Loop through number of rows
                        xx = edgeMarkerWidth
                        while xx < sheetWidth-edgeMarkerWidth: #Loop through bytes of file

                            byteString = ''

                            yy = 0
                            while yy < 8: #Loop through bits of each byte
                                if sheet.getpixel((xx, (7-yy) + (row*8) + edgeMarkerWidth)) > (120):
                                    byteString += '0'
                                    
                                else:
                                    byteString += '1'
                                yy += 1
                                
                            xx += 1

                            buffer.append(int(byteString, 2))
                output.write(buffer)
                output.close()
                    
            else:
                #No, print error
                print('No binsheets found!')
                print('Put binsheets into the input directory and try again')


    #-------------------- Quit Command -------------------- 
    elif command == 'q' or command == 'Q':
        endProgram = True
        



