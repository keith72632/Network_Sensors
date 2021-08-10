from datetime import datetime
import os

FILE_NAME = "logs.txt"

def print_log(socket):
    f = open(FILE_NAME, "a")

    message = 'Connection made with: ' + str(socket.getsockname()) + ' at ' + str(datetime.now()) + '\n' 

    f.write(message)

    file_size = os.path.getsize(FILE_NAME)

    f.close()

    if file_size >= 10000:
        os.system('rm logs.txt; touch logs.txt')
        print(f'{FILE_NAME} deleted')
