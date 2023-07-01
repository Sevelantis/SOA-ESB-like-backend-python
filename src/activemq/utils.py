class SubIdGenerator:
    curr_id: int = 0
    
    @classmethod
    def generate_next(cls):
        cls.curr_id += 1
        return cls.curr_id
