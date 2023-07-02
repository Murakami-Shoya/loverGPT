# TODO 会話の長さをランダムで変更
# TODO 「おやすみ」で会話区切って意味的なまとまりを作る
# TODO boyかgirlかを切り替えられるようにする

import json

def create_io_json(json_file, user='boy', conversation_num=3*2-1):
    """
    input, instruction, output の形式にする
    """
    io_json = []

    with open(json_file) as f:
        chat_json = json.load(f)
    for i in range(0, len(chat_json), conversation_num+1):
        try:
            speaker = lambda _i: 'ユーザ' if chat_json[_i]['speaker'] == user else 'システム'
            input = '\n'.join([f"{speaker(j)}: {chat_json[j]['text']}" for j in range(i, i+conversation_num)])
            output = chat_json[i+conversation_num]['text']
            dict = {"input": input,
                    "instruction": None,
                    "output": output}
            io_json.append(dict)
        except IndexError as e:
            print(e)
            break
    
    with open('io_dataset.json', 'w') as f:
        json.dump(io_json, f, indent=2)