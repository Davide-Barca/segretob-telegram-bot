import os

class User:    
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id
        self.check_folder()
    
    def check_folder(self):
        path = f"./Files/{str(self.id)}"
        # print(str(not os.path.exists(path)) + " | RISULTATO")
        if(not os.path.exists(path)):
            os.mkdir(f'./Files/{str(self.id)}')
            with open("./Files/users.txt", 'a') as new_file:
                new_file.write(f"{str(self.username)} = {str(self.id)}\n")
    
    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username
    
    def get_file_path(self):
        return self.file_path
    
    def set_file_path(self, path):
        self.file_path = path
