import uuid

class FilenameGenerator:
    
    @classmethod
    def generate(
        cls, 
        user_id: int,
        ext: str
        ) -> str:
        return f'userid_{user_id}_{uuid.uuid4().__str__()}.{ext.lower()}'
    