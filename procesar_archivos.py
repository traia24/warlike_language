# Instalar e importar las bibliotecas necesarias
install spacy
install pandas
install six
install --upgrade six
-m spacy download es_core_news_lg
import re
import spacy
import os
import pandas as pd

# 1. Función para limpiar los problemas de puntuación y ortotipografía de los textos del corpus
def limpieza_textos(texto):
    # Patrón de búsqueda para encontrar espacios de no separación entre números y símbolos
    patron = r'(?<=\d)\s*?(?=[^\d\s])|(?<=[^\d\s])\s*?(?=\d)'
    # Reemplazar los espacios de no separación por espacios normales
    texto = re.sub(patron, ' ', texto)
    # Patrón de búsqueda para encontrar espacios de no separación antes de un signo de puntuación
    patron_puntuacion = r'\s*?([^\w\s])'  # Utilizamos [^\w\s] para representar la puntuación
    # Eliminar los espacios de no separación antes de un signo de puntuación
    texto = re.sub(patron_puntuacion, r'\1', texto)
    # Patrón de búsqueda para encontrar dos espacios normales consecutivos al final del texto
    patron_dos_espacios = r'\s{2,}$'
    # Reemplazar dos espacios normales consecutivos por uno solo al final del texto
    texto = re.sub(patron_dos_espacios, ' ', texto)
    # Patrón de búsqueda para encontrar comillas angulares de apertura («)
    patron_comillas_apertura = r'«(\w)'  # Detectar comillas angulares seguidas de una palabra
    # Convertir comillas angulares de apertura a comillas inglesas de apertura y ajustar espacios
    texto = re.sub(patron_comillas_apertura, r' “ \1', texto)
    # Patrón de búsqueda para encontrar comillas angulares de cierre (»)
    patron_comillas_cierre = r'(\w)»'  # Detectar palabra seguida de comillas angulares de cierre
    # Convertir comillas angulares de cierre a comillas inglesas de cierre y ajustar espacios
    texto = re.sub(patron_comillas_cierre, r'\1 ” ', texto)
    # Añadir un espacio delante y detrás de cada símbolo ":"
    texto = re.sub(r':', r' : ', texto)
    # Convertir todas las palabras a minúsculas
    texto = texto.lower()
    return texto

# 2. Función para tokenizar y lematizar las palabras de cada uno de los textos contenidos en el corpus
def tokenizar_lematizar(texto):
    # Cargar el modelo de lenguaje en español
    nlp = spacy.load('es_core_news_lg')
    # Tokenizar y lematizar las palabras en el texto + etiquetación POS
    doc = nlp(texto)
    lemas_etiquetados = [(token.lemma_, token.pos_) for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]]
    lemas = [lemma for lemma, _ in lemas_etiquetados]
    print(lemas_etiquetados)
    return lemas

# 3. Crear la variable 'Vocabulario_referencia'
def Vocabulario_referencia():
    file_path = 'vocabulario_belico_lematizado_v3.txt'
    with open(file_path, 'r') as file:
        vocabulario_referencia = file.read().splitlines()
    return vocabulario_referencia

# 4. Función principal para procesar los archivos de texto
def procesar_archivos():
    # Ruta de la carpeta que contiene los archivos .txt
    carpeta_archivos = 'corpus_prueba/'

    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(carpeta_archivos)

    # Diccionario para almacenar los lemas y frecuencias de aparición de todos los archivos
    lemas_frecuencias = {}

    # Recorrer todos los archivos .txt de la carpeta
    for archivo in archivos:
        # Comprobar si el archivo tiene extensión .txt
        if archivo.endswith('.txt'):
            # Ruta completa del archivo
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            
            # Leer el contenido del archivo
            with open(ruta_archivo, 'r') as file:
                contenido = file.read()

            # Paso 1: Limpieza de los textos del corpus a nivel ortotipográfico y de puntuación
            contenido_limpio = limpieza_textos(contenido)
            #archivo_temporal = open("limpio_"+archivo,"w")
            #print(contenido_limpio, file=archivo_temporal)
            #archivo_temporal.close()

            # Paso 2: Tokenizar, lematizar y etiquetar POS
            lemas = tokenizar_lematizar(contenido_limpio)

            # Paso 3: Identificar las palabras lematizadas que se encuentren en el Vocabulario_referencia
            vocabulario_referencia = Vocabulario_referencia()  # Obtener el Vocabulario_referencia
            lemas_belicos_encontrados = [lema for lema in lemas if lema in vocabulario_referencia]

            # Paso 4: Calcular la frecuencia de aparición de las palabras identificadas
            frecuencia_palabras = {}
            for lema in lemas_belicos_encontrados:
                if lema in frecuencia_palabras:
                    frecuencia_palabras[lema] += 1
                else:
                    frecuencia_palabras[lema] = 1

            # Agregar los lemas y frecuencias al diccionario
            lemas_frecuencias[archivo] = frecuencia_palabras
    
    # Crear un DataFrame a partir del diccionario de lemas y frecuencias
    df = pd.DataFrame(lemas_frecuencias).fillna(0)

    # Agregar una columna con la suma de las frecuencias por archivo
    df['Frecuencia total'] = df.sum(axis=1)

    # Reordenar las columnas, moviendo "Frecuencia total" al principio
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]

    # Imprimir la tabla
    print(df)

    # Recuento de palabras, lemas bélicos y porcentajes
    suma_total_lemas_belicos = df['Frecuencia total'].sum() # Calcular la suma de todos los valores de "frecuencia total"
    total_palabras = sum([len(contenido.split()) for archivo in archivos if archivo.endswith('.txt')])
    porcentaje_lema_belico_corpus = (suma_total_lemas_belicos / total_palabras) * 100

    # Imprimir
    print("Total lemas léxicos en corpus:", total_palabras)
    print("Total de lemas bélicos en corpus:", suma_total_lemas_belicos)
    print("Porcentaje de frecuencia de lemas bélicos en corpus:", porcentaje_lema_belico_corpus)

    for archivo in archivos:
        if archivo.endswith('.txt'):
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            with open(ruta_archivo, 'r') as file:
                contenido = file.read()
            palabras_totales = len(contenido.split())
            lemas_belicos = sum(df[archivo].values)
            porcentaje_lema_belico = (lemas_belicos / palabras_totales) * 100

            print(f"Total lemas léxicos en {archivo}: {palabras_totales}")
            print(f"Total lemas bélicos en {archivo}: {lemas_belicos}")
            print(f"Porcentaje de frecuencia de lemas bélicos en {archivo}: {porcentaje_lema_belico:.2f}%\n\n")

    # Guardar la tabla en un archivo Excel (.xlsx)
    ruta_guardado = 'tabla_de_frecuencias.xlsx'
    df.to_excel(ruta_guardado, index=True)

    # Imprimir mensaje de confirmación
    print("Tabla de frecuencias guardada en:", ruta_guardado)

    # Guardar los resultados en un archivo de análisis
    ruta_analisis = 'analisis.txt'
    with open(ruta_analisis, 'w') as file:
        file.write(f"Total lemas léxicos en corpus: {total_palabras}\n") # Nº de lemas léxicos en todo el corpus
        file.write(f"Total lemas bélicos en corpus: {suma_total_lemas_belicos}\n") # Nº de lemas bélicos en todo el corpus
        file.write(f"Porcentaje de frecuencia de lemas bélicos en corpus: {porcentaje_lema_belico_corpus:.2f}%\n") # % de lemas bélicos sobre total palabras léxicas del corpus

        for archivo in archivos:
            if archivo.endswith('.txt'):
                ruta_archivo = os.path.join(carpeta_archivos, archivo)
                with open(ruta_archivo, 'r') as file_txt:
                    contenido = file_txt.read()
                palabras_totales = len(contenido.split())
                lemas_belicos = sum(df[archivo].values)
                porcentaje_lema_belico = (lemas_belicos / palabras_totales) * 100

                file.write(f"\nTotal lemas léxicos en {archivo}: {palabras_totales}\n")
                file.write(f"Total lemas bélicos en {archivo}: {lemas_belicos}\n")
                file.write(f"Porcentaje de frecuencia de lemas bélicos en {archivo}: {porcentaje_lema_belico:.2f}%\n\n")

    # Imprimir mensaje de confirmación
    print("Análisis guardado en:", ruta_analisis)

# Llamar a la función principal para procesar los archivos
procesar_archivos()