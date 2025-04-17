#! python

# import os

# import sys
# from dotenv import load_dotenv

# # Cargar las variables desde el archivo .env
# load_dotenv()

# # Variables de entorno
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# project_id = os.getenv("PROJECT_ID")
# processor_id = os.getenv("PROCESSOR_ID")
# endpoint = os.getenv("ENDPOINT")

# from google.cloud import documentai
# from google.api_core.client_options import ClientOptions

# def get_text_from_pdf_ocr(file_path):
#     try:
#         mime_type = 'image/jpeg'  # o 'application/pdf'
#         print(mime_type)

#         client = documentai.DocumentProcessorServiceClient(
#             client_options=ClientOptions(api_endpoint=endpoint)
#         )

#         name = client.processor_path(project=project_id, location="us", processor=processor_id)

#         with open(file_path, "rb") as image:
#             image_content = image.read()

#         raw_document = documentai.RawDocument(
#             content=image_content, mime_type=mime_type
#         )

#         request = documentai.ProcessRequest(name=name, raw_document=raw_document)
#         response = client.process_document(request=request)
#         document = response.document
#         return document.text
#     except Exception as e:
#         print("Error:", e)
#         return None

# if __name__ == '__main__':
#     print ('argument list', sys.argv[1])
#     file_path = sys.argv[1]
#     text = get_text_from_pdf_ocr(file_path)
#     print(text)


# import os
# import sys
# from dotenv import load_dotenv
# from google.cloud import vision

# # Cargar variables del archivo .env
# load_dotenv()

# # Variables de entorno
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# def get_text_from_image_ocr(file_path):
#     try:
#         client = vision.ImageAnnotatorClient()

#         with open(file_path, "rb") as image_file:
#             content = image_file.read()

#         image = vision.Image(content=content)
#         response = client.text_detection(image=image)
#         annotations = response.text_annotations

#         if response.error.message:
#             raise Exception(response.error.message)

#         if annotations:
#             return annotations[0].description  # Primer bloque con todo el texto

#         return ""

#     except Exception as e:
#         print("Error:", e)
#         return None

# if __name__ == '__main__':
#     print('argument list', sys.argv[1])
#     file_path = sys.argv[1]
#     text = get_text_from_image_ocr(file_path)
#     print(text)


# import os
# import sys
# from dotenv import load_dotenv
# from google.cloud import vision

# # Cargar variables del archivo .env
# load_dotenv()

# # Variables de entorno
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# def get_ordered_text_blocks(annotations):
#     blocks = []

#     for annotation in annotations[1:]:  # Saltamos el primero (es todo el texto junto)
#         # Extraer coordenadas (vertices del bounding box)
#         vertices = annotation.bounding_poly.vertices
#         x = vertices[0].x if vertices[0].x is not None else 0
#         y = vertices[0].y if vertices[0].y is not None else 0

#         blocks.append({
#             'text': annotation.description,
#             'x': x,
#             'y': y
#         })

#     # Ordenar primero por y, luego por x
#     blocks.sort(key=lambda b: (b['y'], b['x']))

#     # Concatenar texto en orden
#     ordered_text = ' '.join([block['text'] for block in blocks])
#     return ordered_text

# def get_text_from_image_ocr(file_path):
#     try:
#         client = vision.ImageAnnotatorClient()

#         with open(file_path, "rb") as image_file:
#             content = image_file.read()

#         image = vision.Image(content=content)
#         response = client.text_detection(image=image)
#         annotations = response.text_annotations

#         if response.error.message:
#             raise Exception(response.error.message)

#         if annotations:
#             return get_ordered_text_blocks(annotations)

#         return ""

#     except Exception as e:
#         print("Error:", e)
#         return None

# if __name__ == '__main__':
#     print('argument list', sys.argv[1])
#     file_path = sys.argv[1]
#     text = get_text_from_image_ocr(file_path)
#     print(text)


# import os
# import sys
# from dotenv import load_dotenv
# from google.cloud import vision

# # Cargar variables del archivo .env (donde está la ruta a las credenciales de Google)
# load_dotenv()

# # Asignar la variable de entorno necesaria para autenticarse con Google Cloud Vision API
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# def get_text_from_image_ocr(file_path):
#     try:
#         # Crear un cliente para la API de Vision
#         client = vision.ImageAnnotatorClient()

#         # Abrir la imagen en modo binario y leer su contenido
#         with open(file_path, "rb") as image_file:
#             content = image_file.read()

#         # Crear un objeto de imagen para enviarlo a la API
#         image = vision.Image(content=content)

#         # Usar la API para detectar texto estructurado en el documento (mejor para documentos con párrafos/líneas)
#         response = client.document_text_detection(image=image)

#         # Verificar si hubo algún error en la respuesta
#         if response.error.message:
#             raise Exception(response.error.message)

#         # Extraer la anotación completa del texto detectado (estructura del documento)
#         full_text = response.full_text_annotation

#         lines = []  # Aquí se almacenarán las líneas reconstruidas

#         # Recorrer todas las páginas del documento detectado
#         for page in full_text.pages:
#             # Recorrer todos los bloques de texto (pueden ser párrafos, títulos, etc.)
#             for block in page.blocks:
#                 # Recorrer cada párrafo dentro del bloque
#                 for paragraph in block.paragraphs:
#                     line_text = ""  # Inicializar la línea de texto
#                     # Recorrer todas las palabras en el párrafo
#                     for word in paragraph.words:
#                         # Unir los caracteres de cada palabra
#                         word_text = ''.join([symbol.text for symbol in word.symbols])
#                         line_text += word_text + " "  # Agregar la palabra a la línea
#                     lines.append(line_text.strip())  # Agregar la línea terminada a la lista

#         # Devolver todas las líneas unidas por saltos de línea
#         return "\n".join(lines)

#     except Exception as e:
#         # Mostrar cualquier error que ocurra
#         print("Error:", e)
#         return None

# # Punto de entrada del script si se ejecuta desde la línea de comandos
# if __name__ == '__main__':
#     # Obtener el nombre del archivo desde los argumentos del script
#     file_path = sys.argv[1]
#     print('argument list', file_path)

#     # Ejecutar la función para procesar la imagen
#     text = get_text_from_image_ocr(file_path)

#     # Imprimir el texto extraído
#     print(text)


import os
import sys
from dotenv import load_dotenv
from google.cloud import (
    vision_v1p3beta1 as vision,
)  # Versión específica para manuscritos

# Cargar variables del archivo .env
load_dotenv()

# Establecer variable de entorno con la ruta del archivo de credenciales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)


def get_handwritten_text_from_image(file_path):
    try:
        # Crear cliente de la API de Vision
        client = vision.ImageAnnotatorClient()

        # Leer la imagen en binario
        with open(file_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Indicar que esperas texto manuscrito en español TENER EN CUENTA QUE ESTA EN BETA SEGUN INFORMACION DE GOOGLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        image_context = vision.ImageContext(language_hints=["es-t-i0-handwrit"])

        # Usar document_text_detection con contexto de idioma manuscrito
        response = client.document_text_detection(
            image=image, image_context=image_context
        )

        # Verificar errores
        if response.error.message:
            raise Exception(response.error.message)

        # Extraer anotaciones de texto completas
        full_text = response.full_text_annotation

        lines = []
        for page in full_text.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    line_text = ""
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])
                        line_text += word_text + " "
                    lines.append(line_text.strip())

        # Unir las líneas en un solo string
        return "\n".join(lines)

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    file_path = sys.argv[1]
    print("Archivo procesado:", file_path)
    text = get_handwritten_text_from_image(file_path)
    print("\nTexto detectado:\n")
    print(text)


# import os
# import sys
# from dotenv import load_dotenv
# from google.cloud import (
#     vision_v1p3beta1 as vision,
# )  # Specific version for handwriting support

# # Load environment variables from .env file
# load_dotenv()

# # Set the credentials path from environment variable
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
#     "GOOGLE_APPLICATION_CREDENTIALS"
# )


# def get_handwritten_text_from_image(file_path, y_threshold=15):
#     try:
#         # Initialize the Google Cloud Vision client
#         client = vision.ImageAnnotatorClient()

#         # Read the image file as binary
#         with open(file_path, "rb") as image_file:
#             content = image_file.read()

#         image = vision.Image(content=content)

#         # Set language hint to detect Spanish handwriting
#         image_context = vision.ImageContext(language_hints=["es-t-i0-handwrit"])

#         # Perform text detection optimized for documents (and handwriting)
#         response = client.document_text_detection(
#             image=image, image_context=image_context
#         )

#         # Raise an exception if there's an error in the response
#         if response.error.message:
#             raise Exception(response.error.message)

#         # Get the full text annotation
#         full_text = response.full_text_annotation

#         # Store words with their text and coordinates
#         word_list = []

#         for page in full_text.pages:
#             for block in page.blocks:
#                 for paragraph in block.paragraphs:
#                     for word in paragraph.words:
#                         word_text = "".join([symbol.text for symbol in word.symbols])
#                         x = word.bounding_box.vertices[0].x
#                         y = word.bounding_box.vertices[0].y
#                         word_list.append({"text": word_text, "x": x, "y": y})

#         # Group words into lines based on Y position (vertical closeness)
#         lines = []
#         for word in word_list:
#             added = False
#             for line in lines:
#                 if abs(line["y"] - word["y"]) < y_threshold:
#                     line["words"].append(word)
#                     added = True
#                     break
#             if not added:
#                 lines.append({"y": word["y"], "words": [word]})

#         # Sort lines by Y (top to bottom)
#         lines.sort(key=lambda l: l["y"])

#         # Sort words in each line by X (left to right)
#         for line in lines:
#             line["words"].sort(key=lambda w: w["x"])

#         # Reconstruct the text from the sorted words
#         ordered_text = "\n".join(
#             [" ".join([w["text"] for w in line["words"]]) for line in lines]
#         )

#         return ordered_text

#     except Exception as e:
#         print("Error:", e)
#         return None


# if __name__ == "__main__":
#     file_path = sys.argv[1]
#     print("Processed file:", file_path)
#     text = get_handwritten_text_from_image(file_path)
#     print("\nDetected text (ordered by position):\n")
#     print(text)
