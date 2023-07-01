import uuid

class CorrelationIdGenerator:
    
    @classmethod
    def generate(cls) -> str:
        return uuid.uuid4().__str__()
