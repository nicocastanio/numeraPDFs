#!/usr/bin/env python3
# -*- coding: utf-8 -*-

helpDoc = ''' 
Agrega números de página a documentos PDF que se encuentren en una carpeta especificada.

Uso: 
    C:> python numeraPDF.py [carpeta]
Autor: 
    Nicolás Castaño
Versión: 2.2

----------------- Versión Original -----------------
Add Page Number to PDF file with Python
Python 给 PDF 添加 页码
usage:
    python addPageNumberToPDF.py [PDF path]
require:
    pip install reportlab pypdf2
    Support both Python2/3, But more recommend Python3
tips:
    * output file will save at pdfWithNumbers/[PDF path]_page.pdf
    * only support A4 size PDF
    * tested on Python2/Python3@ubuntu
    * more large size of PDF require more RAM
    * if segmentation fault, plaese try use Python 3
    * if generate PDF document is damaged, plaese try use Python 3
Author:
    Lei Yang (ylxx@live.com)
GitHub:
    https://gist.github.com/DIYer22/b9ede6b5b96109788a47973649645c1f
'''

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


#def main(): 


if __name__ == "__main__":
    pass
    import sys,os
    path = 'C:\tmp\\'
    if len(sys.argv) == 1:
        if not os.path.isfile(path):
            sys.exit(1)
    else:
        path = sys.argv[1]
    #base = os.path.basename(path)

    tmp = "__tmp.pdf"

    #batch = 10
    batch = 0
    totPages = 0  # contador global de paginas 
    
    # verificar si existe el path destino, sino lo crea 
    destinationPath = path + 'pdfPaginado\\'
    if not os.path.isdir(destinationPath):
        os.mkdir(destinationPath)
        print('Se creó carpeta: "pdfPaginado"')
                
    # buscar archivos pdf en el directorio actual
    flist = filebrowser("*.pdf", path)
    print('Archivos a procesar: ',flist) 
    newFile1 = destinationPath + 'salidav1.pdf'
    output1 = PdfFileWriter()
    
    # recorrer la lista de Nombres de archivos 
    for file in flist: 
        print('--- Archivo: ', file) 
        base = file 
        filename = path+file

        # abrir Archivo (path completo) para lectura 
        with open(filename, 'rb') as f:
            pdf = PdfFileReader(f,strict=False)
            n = pdf.getNumPages() #cant de pag del pdf actual (original) 

            #if batch == 0:
            batch = -n
            output = PdfFileWriter()
                
            # 
            desde = totPages
            hasta = n+totPages
            createPagePdf(n,tmp,desde,hasta)   # crear pdf en tmp 
            
            # abrir archivo temporal y moverlo 
            with open(tmp, 'rb') as ftmp:
                numberedPdf = PdfFileReader(ftmp)
                
                for p in range(n):
                    #if not p%batch and p:
                    #    newFile = file.replace(base, destinationPath+ base[:-4] + '_page_%d'%(p//batch) + base[-4:])
                    #    print('Destino: ', newFile)
                    #    with open(newFile, 'wb') as f:
                    #        output.write(f)
                    #    output = PdfFileWriter()

                    #print('page: %d of %d'%(p, n))
                    
                    page = pdf.getPage(p) # pagina original 
                    numberLayer = numberedPdf.getPage(p) # pagina numerada 
                    page.mergePage(numberLayer) # merge de ambas paginas 
                    output.addPage(page) # agrego a Salida 
                    
                    output1.addPage(page)
                  
                #print('-nro pages: ',output.getNumPages())
                #if output.getNumPages() == total:
                if output.getNumPages():
                    newFile = file.replace(base, destinationPath+ base[:-4] + '_page_%d'%(p//batch + 1)  + file[-4:])

                    with open(newFile, 'wb') as f:
                        output.write(f)
                    os.remove(newFile)
                
            os.remove(tmp)
            totPages = totPages + n 

        # luego de procesar, eliminamos archivos originales
        #os.remove(filename)

    if output1.getNumPages():
        print('- Salida: ', newFile1)
        with open(newFile1, 'wb') as o:
            output1.write(o)

