"""Module for downloading images"""
import requests


class Picture:
    """Module for downloading images"""
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.picture()

    def picture(self):
        """Attribute allowing to download an image
        according to the name and the link"""
        response = requests.get(self.link)
        picture_file = self.name + '.jpg'
        file = open(picture_file, 'wb')
        file.write(response.content)
        file.close()
