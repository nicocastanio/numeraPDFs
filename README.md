# numeraPDFs
A partir de un directorio que contenga archivos pdfs, crea un nuevo archivo pdf (procesado.pdf) haciendo merge de los archivos encontrados, poniendoles nro de pagina, y lo deja en un directorio "pdfPaginado" dentro del inicial.  

## Requerimientos:
pip install reportlab pypdf2 

## Uso: 
python numerarpdfs.py [folder path] [username]
[folder path] obligatorio
[username] opcional

## Basado en: 
Add Page Number to PDF file with Python
https://gist.github.com/DIYer22/b9ede6b5b96109788a47973649645c1f

## Mejoras:
* folder destino por parametro
* archivo destino por parametro
* incorporar otros nuevos parametros. 
* manejo de errores.