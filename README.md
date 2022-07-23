# BinPrinter
A physical backup solution using python and printer paper.

## How does it work?
BinPrinter does two things:
1. Turn files into "BinSheets" which can then be printed onto regular printer paper
2. Read the binary data from the BitSheets, in order to recreate the file

BinPrinter will accept a file as input (Image, Audio, Video, etc). The binary data from that file is then read, and added to an image in the form of black and white squares (not visually dis-similiar to a QR code). These image files can then be printed onto regular old printer paper, and stored away somewhere as a pysical data backup.

BinPrinter can then accept scans of these sheets as input, and then recreate the file from the binary data on the sheets.

## But why tho?
The actual bits need to be reasoonably large in order to compensate for lower resolution printers and scanners. So there is a physical limit to how much data can be stored on a single sheet of paper. The logical next question is, how much data CAN we store on a single sheet of paper. The current capacity is around 10KB.

So the answer to the question "But why tho?", is "because we can". BinPrinter offers a novel way to create physical backups of data, using commonly available materials, and Python.

## Examples of BinSheets
Some photos of BinSheets for a MOD file for the song Unreal Superhero 3

<img src="https://user-images.githubusercontent.com/108885787/178125893-87950fca-1850-4620-a0dd-4e3744f2ffe8.jpg" width="50%" height="50%" alt="Closeup of a binsheet">
<img src="https://user-images.githubusercontent.com/108885787/178125896-f00e8b04-7fd5-4860-9099-df69273bbf14.jpg" width="50%" height="50%" alt="Data spanning multiple binsheets">
