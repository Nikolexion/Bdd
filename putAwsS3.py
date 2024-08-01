import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

BUCKET_NAME = 'nikotesteo'
FILE_NAME = 'resources/LOGO_LOGISTICA_Y_DISTRIBUCION-1.png'

try:
    data = open(FILE_NAME, 'rb')
    
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

    # Intentar subir el archivo con ACL 'public-read'
    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')

    print("Archivo subido exitosamente con ACL 'public-read'.")
except FileNotFoundError:
    print("El archivo especificado no se encontró.")
except NoCredentialsError:
    print("No se encontraron las credenciales de AWS.")
except PartialCredentialsError:
    print("Las credenciales de AWS están incompletas.")
except Exception as e:
    print(f"Ocurrió un error: {e}")