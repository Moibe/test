import asyncio
import time
import os
from pyppeteer import launch
import config

async def camino(page, estructura):

    print("Bienvenido a todoist!")

    for instancia in config.configuracion:
        url_todoist = instancia["url_todoist"]
        todoist_mail = instancia["todoist_mail"]
        todoist_pass = instancia["todoist_pass"]
        time.sleep(1)

    print("Entrando a la página de inicio de sesión de Todoist...")
    time.sleep(7)
    await page.goto(url_todoist)

    
    print("Cargando página...")
    time.sleep(5)

    #Correo    
    email_input = await page.querySelector('input[type="email"]')
    
      
    time.sleep(1)
    await email_input.type(todoist_mail)

    time.sleep(3)

    #Password
    password_input = await page.querySelector('input[type="password"]')
    await password_input.type(todoist_pass)

    time.sleep(6)

    #Botón Iniciar Sesión
    login_button = await page.querySelector('button[data-gtm-id="start-email-login"]')
    await login_button.click()
    
    await page.waitForNavigation()
    

    #Alta de tareas
    time.sleep(7)
    print("Tareas dadas de alta en todoist:") 
    
    for tarea in estructura:
        print(tarea["titulo"], tarea["descripcion"])

        #Encontrar el botón de nueva tarea y hacer click en él.
        try:
            new_task = await page.querySelector('button.vZhNClH')
            await new_task.click()
        except Exception as error:
            print(f"Ha ocurrido un error: {error}")

        #Encontrar los campos de escritura para la tarea.
        try:
            title_fields = await page.querySelectorAll('p.is-empty')
            time.sleep(5)
            # Si hay al menos dos campos
            if len(title_fields) >= 2:
                # Escribir Título
                await title_fields[0].type(tarea["titulo"])
                # Escribir Descripción
                await title_fields[1].click()
                await title_fields[1].type(tarea["descripcion"])
                time.sleep(2)

            # Si hay menos de dos campos, mostrar un mensaje
            else:
                print("Error.")

        except Exception as error:
            print(f"Ha ocurrido un error: {error}")

        #Encontrar submit button y enviar.
        try:
            submit_button = await page.querySelector('button[data-testid="task-editor-submit-button"]')
            time.sleep(5)
            await submit_button.click()
        except Exception as error:
            print(f"Ha ocurrido un error: {error}")

        time.sleep(3)

    print("Proceso terminado...")
    time.sleep(5)
