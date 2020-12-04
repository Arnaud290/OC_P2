"""Module for downloading images"""
import requests
class Picture:
    """Module for downloading images"""
    @classmethod
    def picture(cls, name, link):
        """Attribute allowing to download an image
        according to the name and the link"""
        response = requests.get(link)
        picture_file = name + '.jpg'
        file = open(picture_file, 'wb')
        file.write(response.content)
        file.close()
