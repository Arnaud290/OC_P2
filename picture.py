import requests
class Picture:    
    
    def picture(self, name, link):
        response = requests.get(link)                                                                                     
        picture_file = name + '.jpg'                                                                                          
        file = open(picture_file, 'wb')
        file.write(response.content)                                                                                                               
        file.close()     