#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import glob


def createPagePdf(num, tmp, desde, hasta):
    c = canvas.Canvas(tmp)
    for i in range(desde+1,hasta+1):   #para que comience de 1
        c.drawString((210//2)*mm, (4)*mm, str(i))
        c.showPage()
    c.save()
    return
    #with open(tmp, 'rb') as f:
    #    pdf = PdfFileReader(f)
    #    layer = pdf.getPage(0)
    #return layer


def filebrowser(word, folder):
    """Returns a list with all files with the word/extension in it"""
    file = []
    # print('ext:', word) 
    # print('folder:', folder )
    for f in glob.glob1(folder, word):
        file.append(f)
    #for f in glob.glob("*"):
        #if word in f:
            #file.append(f)
    return file


def main(folder): 
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
        createPagePdf(n,tmp,desde,hasta)   # crear pdf Numerado en tmp 

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
    if len(sys.argv) == 1:
        if not os.path.isfile(path):
            sys.exit(1)
    else:
        path = sys.argv[1]

    main(path)