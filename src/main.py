import settings
from create_datset_from_line import *
from prompt import create_io_json, prepare_dataset
from train import load_model, my_train

from pprint import pprint

def main():
    train_dataset, val_dataset = prepare_dataset('/code/io_dataset.json', settings.tokenizer)
    model, trainer = load_model(settings.model_name, train_dataset, val_dataset)
    my_train(model, trainer)

def create_dataset(txt_file):
    txt_list = txt_to_list(txt_file)
    extracted_list = extract_only_chat(txt_list)
    extracted_list = flatten_multiline(extracted_list)
    extracted_list = concat_and_detail(extracted_list)
    # extracted_list = finalize_processing(extracted_list)
    convert_to_json(extracted_list, boy_name=settings.boy_name, girl_name=settings.girl_name)
    create_io_json('/code/chat_dataset.json')

if __name__ == '__main__':
    main()
    # test()
    # create_dataset('/code/talk_dataset.txt')

    