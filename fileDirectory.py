import os





def checkAndCreadDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
