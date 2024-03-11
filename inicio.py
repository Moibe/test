import asyncio
import time
import os
import funciones
from pyppeteer import launch
import todoist

async def main():

    print("¡Bienvenido al manejedor de tareas Trello-Todoist! ✨")
 
    browser, page = await funciones.crearNavegador()

    contenido_listas = await funciones.obtenerListasTareas(page)
 
    print()
    print("Elige una opción:")
    time.sleep(3)

    # Opciones para el usuario
    opciones = {
        "1": "Subir a todoist las tareas de una lista en particular.",
        "2": "Subir a todoist todas las tareas de Trello.",
    }

    # Mostrar las opciones al usuario
    for numero, opcion in opciones.items():
        print(f"{numero}: {opcion}")

    # Pedir al usuario que elija una opción
    while True:
        opcion_elegida = input("Introduzca el número de la opción deseada: ")
        if opcion_elegida in opciones:
            break
        print("Opción no válida. Introduzca 1 o 2.")

    # Seleccionar la acción según la opción elegida
    if opcion_elegida == "1":
        # Subir tareas de una lista en particular
        print("Elegiste subir las tareas de una lista de Trello en particular, elige de que lista:")
        time.sleep(2)
        print()
        #os.system('cls' if os.name == 'nt' else 'clear')
        estructura = await funciones.imprimirListas(page, contenido_listas)
        time.sleep(5)
        pass

    elif opcion_elegida == "2":
        # Subir tareas de la lista total
        print("Elegiste subir tareas del total de todas tus tareas de Trello.")
        time.sleep(2)
        print()
        #os.system('cls' if os.name == 'nt' else 'clear')
        #No hay filtro, imprimirá todas las tareas de todas las listas.
        filtro = ""
        estructura = await funciones.obtenerTareasdeListas(page, contenido_listas, filtro)
        pass

    time.sleep(2)

    print("Listo!, Éstas son las tareas que subiremos a todoist:")
    time.sleep(7)
    print(estructura)
    time.sleep(5)
    

    print("Redirigiendo a Todoist:")
    time.sleep(5)

    await todoist.camino(page, estructura)

    await browser.close()

    print("Las tareas han subido exitosamente a Todoist. Gracias.")
    
asyncio.run(main())
