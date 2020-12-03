import os
from settings import parent_directory
class Repertory:

    def repertory(self, repertory_name):
        os.chdir(parent_directory)
        if not os.path.exists(repertory_name):                                                                                      
            os.makedirs(repertory_name)                                                                                                
        os.chdir(repertory_name)  