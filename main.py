import sys
import os
from threading import *
from threads import *

def main():
    pid = os.getpid()
    print(f'Process I.D.: {pid}')
    t1 = Thread(target=socket_thread)
    t2 = Thread(target=sensor_thread)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(1)
