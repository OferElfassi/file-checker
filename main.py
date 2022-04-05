from datetime import datetime
import os


def check_files():
    directory = '/home/ubuntu/projects/uploads'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)


if __name__ == '__main__':
    print("CRON executed at - \n")
    print(datetime.now().strftime("%D %H:%M:%S"))
    check_files()
