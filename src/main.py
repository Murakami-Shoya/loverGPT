import settings
from create_datset_from_line import *

from pprint import pprint

def main():
    # print(settings.boy_name, settings.girl_name)
    pass

def create_dataset(txt_file):
    txt_list = txt_to_list(txt_file)
    extracted_list = extract_only_chat(txt_list)
    extracted_list = flatten_multiline_and_concat(extracted_list)
    convert_to_json(extracted_list, boy_name=settings.boy_name, girl_name=settings.girl_name)

    # pprint(extracted_list[0:10])
    

if __name__ == '__main__':
    # main()
    create_dataset('./small_chat_dataset.txt')