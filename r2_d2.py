# -*- coding: utf-8 -*

#Librerias
import win32com.client
from pywintypes import com_error
from PyPDF2 import PdfFileMerger
from PIL import Image, ImageFont, ImageDraw
from lib2to3.pgen2 import driver
from ssl import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ssl
import time
import pandas as pd
import numpy as np
import socket
import qrcode
import wget
import os

ssl._create_default_https_context = ssl._create_unverified_context

socket.setdefaulttimeout(30)

parent_dir = os.getcwd() #Obtener directorio actual
os.chdir(parent_dir) #Acceder a directorio actual

r2d2 = pd.DataFrame(columns=['idGamma', 'r2d2'])
ss = pd.DataFrame(columns=['idGamma', 'ss'])

directory = "27_Oct_Papeletas" # Nombre del directorio en donde se guardaran nuestras papeletas, ss, el merge de archivos y la factura final

print(r2d2)
print(ss)

r2d2 = r2d2.append({'idGamma': 'test', 'r2d2': 'test'}, ignore_index=True)
ss = ss.append({'idGamma': 'test', 'ss': 'test'}, ignore_index=True)
print(r2d2)
print(ss)

ss

listado = pd.read_excel(parent_dir + "\\Oct_27.xlsx") # Listado donde se encuentran los IDs de los dispositivos que se les generará papeleta
listado.rename(columns = {'iotDevice': 'Id'}, inplace = True)
listado.head(3)

metersList = pd.read_excel('Concentrado.xlsx') # Listado donde se encuentran los identificadores de cada uno de los gabinetes
metersList

mwwetersList = pd.merge(listado, metersList, on = ['Id'], how = 'left')
metersList.dropna(subset = ['cabinet'], inplace=True)
metersList

#CREACIÓN DE CARPETA DE DESCARGAS
path = os.path.join(parent_dir, directory)
print("Directory '% s' created" % directory)
os.chdir(path)
print(path)

cabinetList = metersList.groupby( [ "Id", "cabinet"] ).count().reset_index()
cabinetList = cabinetList[['Id', 'cabinet', 'latitude']]
cabinetList.rename(columns = {'latitude': 'meters'}, inplace = True)
cabinetList = cabinetList[['Id', 'cabinet', 'meters']]
count = 0
cabinetList = pd.merge(listado, cabinetList, on = ['Id'], how = 'left')
cabinetList

def R2D2(idGamma, df):
    
    url = "https" + idGamma   #Accedemos la página donde yacen las papeletas añadiendo un "/" + ID del dispositivo
    print("         »»»  Descargando        \u2592\u2588\u2592\u2588\u2592\u2588\u2592\u2588")
    
    try:
        wget.download(url, out = path)
        print("\n         »»»  Reporte Descargado     \u2714")
        df = df.append({'idGamma': idGamma, 'r2d2': 'ok'}, ignore_index=True)
        time.sleep(1)
        #work_sheets = sheets.Worksheets[0]
        
        WB_PATH = path + '//' + idGamma + '.xlsx'
        PATH_TO_PDF = path + '//' + idGamma + '_report.pdf'
        
        try:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            print('Start conversion to PDF')
        
            wb = excel.Workbooks.Open(WB_PATH)
            wb.Worksheets(1).Select()
            wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)    
        except com_error as e:
            print("failed.")
        else:
            print("Succeeded.")
            print("\n         »»»  Reporte PDF            \u2714")
        finally:
            wb.Close()
            excel.Quit()
            time.sleep(3)        
            os.remove(path + '\\' + idGamma + '.xlsx')
        
    except:
        print("         »»»  Error en Descarga      \u2717")
        df = df.append({'idGamma': idGamma, 'r2d2': 'error'}, ignore_index=True)
        
    return idGamma + '_report.pdf'

path

def openVPN(): 
    #Opciones de navegación
    Options = webdriver.ChromeOptions()
    #Options.add_argument('--headless')
    Options.add_argument('--start-maximized')
    Options.add_argument('--disable-extensions')
    
    driver_path  = os.getcwd() + "\\chromedriver.exe"
    
    driver = webdriver.Chrome(driver_path, chrome_options=Options)
    
    #Iniciarla en la pantalla 2
    driver.set_window_position(1000, 0)
    driver.maximize_window() 
    time.sleep(10)
    
    #Inicializa el navegador
    driver.get('http://') # Inicializa en la página de la VPN
    
    #Login SiNaMed
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div/div/form/div[1]/input')))\
        .send_keys("user")
    
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div/div/form/div[2]/input')))\
        .send_keys("password")
    
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div/div/form/div[3]/button')))\
        .click()
    time.sleep(10)
    
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div[1]/div[1]/div[2]/ul/li[3]')))\
        .click()
    time.sleep(10)
    
    return driver

def mergePDF(x, finalPDF):
    
    merger = PdfFileMerger()

    for element in x:
        merger.append(element)

    merger.write(finalPDF)
    merger.close()

def ss(idGamma, cabinet, qrInfo, txtInfo, df, driver, a):            
        # Escribe el ID del gabinete
        WebDriverWait(driver, 10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/input')))\
            .send_keys(cabinet)
        # Presiona Buscar
        WebDriverWait(driver, 10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/button[1]')))\
            .click()
        time.sleep(10)
        
        try:
            
            if meters < 7:
            
                # Presiona el ID del Gabinete
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/table/tbody/tr/td[1]/span')))\
                    .click()
                time.sleep(10)
            
                # Pestaña de medidores
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/ul/li[2]/span[2]')))\
                    .click()
                time.sleep(10)
            
                # Screenshot
                imageName = idGamma + ".png"
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]')))\
                    .screenshot(imageName)
        
                image1 = Image.open(path + '/' + imageName)
                img_bg = Image.open(path + '/' + imageName)
                
                print("         »»»  Inicio QR              \u2714")
                
                qr = qrcode.QRCode(box_size=2)
                qr.add_data(qrInfo)
                qr.make()
                img_qr = qr.make_image()
                
                
                pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
                print("         »»»  QR Agregado            \u2714")
                img_bg.paste(img_qr, pos)
                im_name = (imageName)
                img_bg.save((path + '/' + imageName))
                
                image1 = Image.open(path + '/' + imageName)
                
                print("         »»»  Check Point            \u2714")
                
                image_editable = ImageDraw.Draw(image1)
                
                # SCREEN CONFIG
                title_font = ImageFont.truetype(os.getcwd() + "\\Nunito-Light.ttf", 14)
                
                image1.save((path + '/' + imageName))
                print("         »»»  TXT Agregado           \u2714")
                # Convert 2 PDF
                image1 = Image.open(path + '/' + imageName)
                im1 = image1.convert('RGB')
                ss1 = idGamma + '.pdf'
                im1.save(path + '/' + ss1)
                os.remove(path + '/' + imageName)
                          
                print("         »»»  Captura Guardada       \u2714    1")
            
            else:
                
                # Presiona el ID del Gabinete
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/table/tbody/tr/td[1]/span')))\
                    .click()
                time.sleep(1)
            
                # Pestaña de medidores
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/ul/li[2]/span[2]')))\
                    .click()
                time.sleep(10)
                    
                # Screenshot
                imageName = idGamma + ".png"
                
                meter = WebDriverWait(driver, 10)\
                            .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]')))\
                
                driver.execute_script("arguments[0].style='height: 1200px; opacity: 1; display: block;'", meter)
                
                meter.screenshot(imageName)
        
                image1 = Image.open(path + '/' + imageName)
                img_bg = Image.open(path + '/' + imageName)
                
                print("         »»»  Inicio QR              \u2714")
                
                qr = qrcode.QRCode(box_size=2)
                qr.add_data(qrInfo)
                qr.make()
                img_qr = qr.make_image()
                
                
                pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
                print("         »»»  QR Agregado            \u2714")
                img_bg.paste(img_qr, pos)
                im_name = (imageName)
                img_bg.save((path + '/' + imageName))
                
                image1 = Image.open(path + '/' + imageName)
                
                print("         »»»  Check Point            \u2714")
                
                image_editable = ImageDraw.Draw(image1)
                
                # SCREEN CONFIG
                title_font = ImageFont.truetype(os.getcwd() + "\\Nunito-Light.ttf", 14)
                
                image1.save((path + '/' + imageName))
                print("         »»»  TXT Agregado           \u2714")
                #convert PDF
                image1 = Image.open(path + '/' + imageName)
                im1 = image1.convert('RGB')
                ss1 = idGamma + '.pdf'
                im1.save(path + '/' + ss1)
                os.remove(path + '/' + imageName)
                          
                print("         »»»  Captura Guardada       \u2714    1")
            
            #Presiona x para cerrar la tabla
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/button/span')))\
                .click()
            
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/input')))\
                .clear()
            time.sleep(5)
            
            print(str(ss1))
            files = [ss1, os.getcwd() + "\\blank.pdf"]
            merge = idGamma + '_ss.pdf'
            mergePDF(files, merge)
            os.remove(ss1)
            
            return merge

            
        except:
              
            WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/input')))\
                    .clear()
            time.sleep(5)
            print("         »»»  Error en Captura       \u2717")
            
        time.sleep(5)

"""# Modificación para la parte de ss de gammas en pagina de la vpn"""

# Nos quedamos con enteros /// ESTO SE MODIFICARÁ EN VERSIÓN POSTERIOR

cabinet_test = cabinetList.copy() # Copia para no quedarnos en la misma dir de memoria
cabinet_test = cabinet_test.dropna(subset=["cabinet"]) # Eliminamos la parte de nan en el df
cabinet_test['cabinet'] = cabinet_test['cabinet'].astype(int) # Pasamos la info de floats a ints
cabinet_test['meters'] = cabinet_test['meters'].astype(int)
# Para eliminar los nan, y quedarnos con filas con información

cabinet_test = cabinet_test.reset_index(drop=True)

# Para el test
# Tomaremos el index=0 para gamma, gabinete y medidores
gamma_example = str(cabinet_test.Id[0])
cabinet_example = str(cabinet_test.cabinet[0])
meters_example = str(cabinet_test.meters[0])

print(gamma_example, " / ", cabinet_example, " / ", meters_example)

"""# Para Chrome"""

if __name__ == '__main__':
    
    reports = []
    screens = []
    
    count = 0
    driver = openVPN()
    
    for index, row in cabinet_test.iterrows():
        
        try: 
            count+= 1
            a = str(count)
            idGamma = str(row['Id'])
            cabinet = str(row['cabinet'])
            meters = row['meters']
            print('GAMMA: ' + idGamma + '           ' + str(count))
            
            df = metersList[(metersList.Id == idGamma)]
            qr_meters = ''
            
            for index, row in df.iterrows():
    
                qr_meters = qr_meters + str(int(row['position'])) + '     ' + row['meter'] + '\n'
        
            qrInfo = 'Gabinete: ' + cabinet + '\n\n' + 'Medidores: ' + '\n' + qr_meters + '\n\n'
            txtInfo = 'Gabinete: ' + cabinet + '\n\n' + 'Medidores: ' + '\n' + qr_meters + '\n\n'
            print("         »»»  QR TXT                 \u2714")
            
            reports.append(R2D2(idGamma, r2d2))
            screens.append(ss(idGamma, cabinet, qrInfo, txtInfo, ss, driver, a))
            
        except:
            
            print("         »»»  Reporte Sin Info       \u2717")

reports

screens

#Para unir reporte con su respectiva ss

from PyPDF2 import PdfMerger

names = []

for i in range (0, len(cabinet_test)):
    
    pdfs = [cabinet_test.Id[i] + "_report.pdf", cabinet_test.Id[i] + "_ss.pdf"]
    merger = PdfMerger()
    
    for pdf in pdfs:
        merger.append(pdf)
    
    names.append(cabinet_test.Id[i] + ".pdf")
    
    merger.write(cabinet_test.Id[i] + ".pdf")
    merger.close()

names

#Para unir los reportes completos entre sí

pdfs = names
merger = PdfMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write("Factura_New.pdf")
merger.close()

#Eliminar archivos auxiliares

for i in range (0, len(reports)):
    os.remove(reports[i])
    os.remove(screens[i])