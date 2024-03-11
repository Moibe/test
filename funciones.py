import asyncio
from pyppeteer import launch
import time
import config
import sys

async def crearNavegador(): 
    
    for instancia in config.configuracion:
        headless = instancia["headless"]
        url = instancia["url_trello"]
        chromium_path = instancia["chromium_path"]
        time.sleep(2)

    print(f"...Obteniendo listas desde: {url}")
    print()

    try:
            browser = await launch(headless=headless, executablePath=chromium_path)
          
    except Exception as error:
        print(f"Ha ocurrido un error: {error}")
        time.sleep(5)
        print("Un error con el path de su instalación de Chromium causo éste fallo.")
        time.sleep(5)
        print("Considerar editar el archivo config.py antes de correr éste programa.")
        time.sleep(5)
        print("Ya que por default el path de la configuración viene vacío.")
        time.sleep(5)
        print("Si no tienes Chromium puedes bajar la versión más actual en: https://www.chromium.org/")
        time.sleep(5)
        print("Para corregir éste error editar ésta línea de código en el archivo config.py:")
        time.sleep(5)
        print('"chromium_path": "",')
        time.sleep(5)
        print('Ejemplo: "chromium_path": "D:\Chromium\chrome.exe" ')
        time.sleep(5)
        print("Ir a archivo readme.md para más información.")
        time.sleep(10)
        sys.exit(1)

    page = await browser.newPage()
    await page.goto(url)

    #Quitar botón para dar visibilidad cuando está en Headless = False.
    button = await page.querySelector("button[data-testid='about-this-board-modal-cta-button']")
    await button.click()

    #Quitar tache.
    tache = await page.querySelector("a.board-menu-header-close-button")
    await tache.click()

    return browser, page


async def obtenerListasTareas(page):

    #IMPRESION DE NOMBRE DE TODAS LAS LISTAS
    contenido_listas = []
    elementos_listas = await page.querySelectorAll("[data-testid='list-name']")
    
    print(f"Tienes {len(elementos_listas)} listas de Trello:")
    print()
    time.sleep(4)

    for lista in elementos_listas:
         title = await page.evaluate('(element) => element.textContent', lista)
         contenido_listas.append(title)
    
    print(contenido_listas)
    time.sleep(3)

    return contenido_listas

async def imprimirListas(page, contenido_listas):

    # Convertir la variable a una lista numerada
    lista_numerada = []
    for indice, elemento in enumerate(contenido_listas):
        lista_numerada.append(f"{indice + 1}. {elemento}")

    # Mostrar la lista al usuario
    for elemento in lista_numerada:
        print(elemento)

    # Obtener la selección del usuario
    seleccion_usuario = input("Introduce el número de la opción que deseas elegir: ")

    # Obtener el elemento seleccionado
    elemento_seleccionado = contenido_listas[int(seleccion_usuario) - 1]

    # Ejecutar la función con la selección del usuario
    estructura = await obtenerTareasdeListas(page, contenido_listas, elemento_seleccionado)

    return estructura


async def obtenerTareasdeListas(page, contenido_listas, filtro):
   
    total = []
    elementos_listas = await page.querySelectorAll("[data-testid='list-cards']")
    
    numero = 0
    
    for lista in elementos_listas:
         
         nombre_lista = contenido_listas[numero]
         
         elementos_tareas = await lista.querySelectorAll("[data-testid='card-name']")

         for card in elementos_tareas:
            task = await page.evaluate('(element) => element.innerText', card)
            total.append([nombre_lista, task])
         numero += 1


    #Imprimir la lista total de tareas y numerarlas.
    estructura = []
    #contador = 1

    if filtro == "": 
        for fila in total:
            print(f"{fila[0]} - {fila[1]}")
            time.sleep(1)
            nuevo_elemento = {
                "titulo": fila[0],
                "descripcion": fila[1]
            }
            estructura.append(nuevo_elemento)
            print("Preparando para subir a todoist.")
            time.sleep(2)
            #contador += 1
        time.sleep(1)

    else:
        for fila in total:
            if fila[0] == filtro: 
                print(f"{fila[0]} - {fila[1]}")
                time.sleep(1)
                nuevo_elemento = {
                "titulo": fila[0],
                "descripcion": fila[1]
            }
                estructura.append(nuevo_elemento)
                print("Preparando para subir a todoist.")
                time.sleep(2)
            #contador += 1
            
        time.sleep(1)

    return estructura