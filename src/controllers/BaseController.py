import os

class BaseController:
    
    def __init__(self):

        
        self.base_dir = os.path.dirname( os.path.dirname(__file__) )

        self.database_dir = os.path.join(
            self.base_dir,
            "assets/vectordb"
        )
        
   

    def get_database_path(self, db_name: str):

        database_path = os.path.join(
            self.database_dir, db_name
        )

        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path