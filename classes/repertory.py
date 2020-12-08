"""Module for the creation of directories"""
import os


class Repertory:
    """Module for the creation of directories"""
    def __init__(self, repertory_name):
        self.repertory_name = repertory_name
        self.repertory()

    def repertory(self):
        """Attribute for the creation of a
        directory according to the name"""
        if not os.path.exists(self.repertory_name):
            os.makedirs(self.repertory_name)
        os.chdir(self.repertory_name)
