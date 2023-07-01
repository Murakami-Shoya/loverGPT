import json
import re

def txt_to_list(txt_file: str) -> list:
    f = open(txt_file, 'r')
    txt_list = f.readlines()
    f.close()
    return txt_list

def extract_only_chat(txt_list: list) -> list:
    """
    日付、改行、写真、スタンプの行を削除
    電話、不在着信、絵文字の削除、リンク
    """
    extracted_list = []
    deleted_re = re.compile(r'(^\d{4}\/\d{2}\/\d{2})|(^\n)|(^\")|\[写真\]|\[スタンプ\]|☎|https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)\'\[\]]+')
    deleted_sub_re = re.compile(r'[ .0-9a-zA-Z]*\(([\\!"#\\$%&\'\()*+,-./:;<=>?@\[\]^_`{}~ ﾟ「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％∀▽´｀┐εཀ∠]+[0-9a-zA-Z]*)+\)[ .0-9a-zA-Z]*')

    for row in txt_list:
        if not (deleted_re.search(row)):
            extracted_list.append(deleted_sub_re.sub('', row))

    return extracted_list

def flatten_multiline_and_concat(txt_list: list) -> list:
    """
    複数行のチャットを一つにまとめる
    連続した人のチャットは\nで区切って結合する
    """
    i = 0
    pre_name = ""
    chat_head_re = "\d{2}:\d{2}\t"   # チャットは00:00のフォーマットで始まる

    while i < len(txt_list):
        # 2行以上になっているチャットを1行に
        if not (re.match(chat_head_re, txt_list[i])):
            txt_list[i-1] = txt_list[i-1] + txt_list[i]
            txt_list.remove(txt_list[i])
            continue

        # 交互に1つずつのチャットなるように(A→B→A→B→…)
        # チャットのフォーマットは [00:00	名前	内容]
        try:
            _, name, message = txt_list[i].split("\t", 2)
            if(name == pre_name):
                txt_list[i-1] = txt_list[i-1] + message
                txt_list.remove(txt_list[i])
            else:
                pre_name = name
                i += 1
        except:
            print(txt_list[i])
            

    return txt_list

def convert_to_json(lst:list, boy_name:str, girl_name:str) -> None:
    dict_list = []

    dict = {"time": "", "speaker": "", "text": ""}
    for i in range(0, len(lst)):
        line = lst[i].strip()
        time, name, message = line.split("\t", 2)

        dict['time'] = time
        dict["text"] = message
        if name == boy_name:
            dict["speaker"] = "boy"
        elif name == girl_name:
            dict["speaker"] = "girl"
        dict_list.append(dict.copy())

    with open('chat_dataset.json', 'w') as f:
        json.dump(dict_list, f, indent=2)
    