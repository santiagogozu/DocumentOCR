import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()

# Variables de entorno
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("PROJECT_ID")
processor_id = os.getenv("PROCESSOR_ID")
endpoint = os.getenv("ENDPOINT")

from google.cloud import documentai
from google.api_core.client_options import ClientOptions

def get_text_from_pdf_ocr(file_path):
    try:
        mime_type = 'image/jpeg'  # o 'application/pdf'
        print(mime_type)

        client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=endpoint)
        )

        name = client.processor_path(project=project_id, location="us", processor=processor_id)

        with open(file_path, "rb") as image:
            image_content = image.read()

        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )

        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        response = client.process_document(request=request)
        document = response.document
        return document.text
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == '__main__':
    file_path = 'test2.jpg'
    text = get_text_from_pdf_ocr(file_path)
    print(text)
