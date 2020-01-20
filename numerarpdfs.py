#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import glob
from datetime import datetime


def createPagePdf(num, tmp, desde, hasta, username):
    c = canvas.Canvas(tmp)
    now = datetime.now()
    now_formated = now.strftime("%d/%m/%Y %H:%M:%S")
    if len(username):
        username = username.upper() + ' - '
    for i in range(desde+1,hasta+1):   #para que comience de 1
        c.drawString((10)*mm, (4)*mm, username+now_formated)
        c.drawString((210//2)*mm, (4)*mm, str(i))
        c.drawString((160)*mm, (4)*mm, "Impreso desde SAP")
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
    tmp = "__tmp.pdf"
    totPages = 0  # contador global de paginas 
    
    # verificar si existe el path destino, sino lo crea 
    destinationPath = path + 'pdfPaginado\\'
    if not os.path.isdir(destinationPath):
        os.mkdir(destinationPath)
        print('Se creó carpeta: "pdfPaginado"')

    # buscar archivos pdf en el directorio actual
    flist = filebrowser("*.pdf", path)
    print('Archivos a procesar: ',flist) 

    # definir salida 
    newFile1 = destinationPath + 'procesado.pdf'
    output1 = PdfFileWriter()

    # recorrer la lista de Nombres de archivos 
    for file in flist: 
        print('--- Archivo: ', file) 
        filename = path+file

        # abrir Archivo (path completo) para lectura 
        pdf = PdfFileReader(filename) # ,strict=False)
        n = pdf.getNumPages() # cant de pag del pdf actual (original) 

        desde = totPages
        hasta = n+totPages
        createPagePdf(n,tmp,desde,hasta, username)   # crear pdf Numerado en tmp 

        # abrir archivo temporal y agregar paginas a salida  
        numberedPdf = PdfFileReader(tmp)
            
        for p in range(n):
            page = pdf.getPage(p) # pagina original 
            numberLayer = numberedPdf.getPage(p) # pagina numerada 
            page.mergePage(numberLayer) # merge de ambas paginas 

            output1.addPage(page) # agrego a Salida 

        # eliminar archivo temporal 
        os.remove(tmp)
        totPages = totPages + n 

        # eliminar archivos originales 
        os.remove(filename)

    if output1.getNumPages():
        print('- Salida: ', newFile1)
        with open(newFile1, 'wb') as o:
            output1.write(o)


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
        if len(sys.argv) == 3:
            username = sys.argv[2]

    main(path,username)

""" 
TO-DO :
- incorporar algunos parametros a la ejecución. ej: help, destino, print, etc 

"""