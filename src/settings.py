import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

boy_name = conf['dataset']['boy_name']
girl_name = conf['dataset']['girl_name']