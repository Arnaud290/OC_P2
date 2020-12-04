"""Module for the creation of directories"""
import os
from settings import parent_directory
class Repertory:
    """Module for the creation of directories"""
    @classmethod
    def repertory(cls, repertory_name):
        """Attribute for the creation of a
        directory according to the name"""
        os.chdir(parent_directory)
        if not os.path.exists(repertory_name):
            os.makedirs(repertory_name)
        os.chdir(repertory_name)
