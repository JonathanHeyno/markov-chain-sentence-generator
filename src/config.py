import os

dirname = os.path.dirname(__file__)


#Paths if Windows environment
if os.name == "nt":
    dirname = dirname[0:len(dirname)-3]

    if not os.path.exists(dirname+'\\sourcedata'):
        os.makedirs(dirname+'\\sourcedata')

    SOURCE_FILE_PATH = os.path.join(dirname, 'sourcedata\\')

#Paths if not Windows envionment
else:

    dirname = dirname[0:len(dirname)-3]
    if not os.path.exists(dirname + '/sourcedata/'):
        os.makedirs(dirname + '/sourcedata/')

    SOURCE_FILE_PATH = os.path.join(dirname, 'sourcedata/')
