#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from pypdf import PdfWriter, PdfReader
import glob
from datetime import datetime


def createPagePdf(tmp, from_page, to_page, username):
    c = canvas.Canvas(tmp)
    # c.setFontSize()
    c.setFont("Helvetica-Oblique",10)
    
    now = datetime.now()
    now_formated = now.strftime("%d/%m/%Y %H:%M:%S")
    if len(username):
        username = username.upper() + ' - '

    for i in range(from_page+1,to_page+1):   #para que comience de 1
        c.drawString((10)*mm, (4)*mm, "Impreso desde SAP por "+username+now_formated)
        c.drawString((165)*mm, (4)*mm, "Página: "+str(i))
        c.showPage()

    c.save()
    return


def filebrowser(word, folder):
    """Returns a list with all files with the word/extension in it"""
    file = []
    for f in glob.glob1(folder, word):
        file.append(f)
    return file


def main(folder, username=''): 
    tmpPdfFile = "__tmp.pdf"
    totPages = 0  # contador global de paginas 
    
    # verificar si existe el path destino, sino lo crea 
    destinationPath = path + 'pdfPaginado\\'
    if not os.path.isdir(destinationPath):
        os.mkdir(destinationPath)
        print('New folder created: "pdfPaginado"')

    # buscar archivos pdf en el directorio actual por orden alfabetico 
    flist = filebrowser("*.pdf", path)
    print('Input files: ',flist) 

    # definir salida 
    newFilename = destinationPath + 'numerado.pdf'
    mergedPdf = PdfWriter()

    # recorrer la lista de Nombres de archivos (orden alfabetico)
    for file in flist: 
        print('--- Processing file: ', file) 
        filename = path+file

        # abrir Archivo (path completo) para lectura 
        originalPdfFile = PdfReader(filename) # ,strict=False)
        n = len(originalPdfFile.pages)
        fromPage = totPages
        toPage = n+totPages

        # crea pdf temporal en blanco, pero numerado. 
        createPagePdf(tmpPdfFile,fromPage,toPage, username)
        numberedPdf = PdfReader(tmpPdfFile)
        
        # recorrer las paginas y hacer merge de original y numerada 
        for p in range(n):
            originalPage = originalPdfFile.pages[p] 
            numberedPage = numberedPdf.pages[p]
            originalPage.merge_page(numberedPage) 
            mergedPdf.add_page(originalPage)

        totPages = totPages + n 
        os.remove(tmpPdfFile)
        os.remove(filename)

    if len(mergedPdf.pages):
        print('- Output: ', newFilename)
        with open(newFilename, 'wb') as f:
            mergedPdf.write(f)


if __name__ == "__main__":
    pass
    import sys,os
    path = 'C:\tmp\\'
    username = ''
    if len(sys.argv) == 1:
        print("C:> python numeraPDF.py [carpeta] [username]")
        if not os.path.isfile(path):
            sys.exit(1)
    else:
        path = sys.argv[1]
        if not os.path.isdir(path):
            print("Carpeta seleccionada no existe.")
        if len(sys.argv) == 3:
            username = sys.argv[2]

    main(path,username)

""" 
TO-DO :
- incorporar algunos parametros a la ejecución. ej: help, destino, print, etc 
- manejo de errores: ejemplo carpeta no existe. 
"""
