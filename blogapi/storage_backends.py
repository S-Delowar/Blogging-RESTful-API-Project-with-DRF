from storages.backends.s3boto3 import S3ManifestStaticStorage

class StaticStorage(S3ManifestStaticStorage):
    location = 'static'

class MediaStorage(S3ManifestStaticStorage):
    location = 'media'
    file_overwrite = False
