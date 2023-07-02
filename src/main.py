import settings
from create_datset_from_line import *
from prompt import create_io_json

from pprint import pprint

def main():
    pass

def create_dataset(txt_file):
    txt_list = txt_to_list('./small_chat_dataset.txt')
    extracted_list = extract_only_chat(txt_list)
    extracted_list = flatten_multiline(extracted_list)
    extracted_list = concat_and_detail(extracted_list)
    # extracted_list = finalize_processing(extracted_list)
    convert_to_json(extracted_list, boy_name=settings.boy_name, girl_name=settings.girl_name)
    create_io_json('/code/chat_dataset.json')

if __name__ == '__main__':
    main()
    # test()
    # create_dataset('./small_chat_dataset.txt')