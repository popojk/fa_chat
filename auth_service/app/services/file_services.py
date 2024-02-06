from fastapi import UploadFile

class FileServices:

    def __init__(self):
        pass

    async def save_avatar(self, file: UploadFile):
        with open(f'uploads/{file.filename}', 'wb') as buffer:
            buffer.write(await file.read())
        return f'uploads/{file.filename}'