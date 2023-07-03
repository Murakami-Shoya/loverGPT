# TODO 会話の長さをランダムで変更
# TODO 「おやすみ」で会話区切って意味的なまとまりを作る
# TODO boyかgirlかを切り替えられるようにする

import json
import settings

def create_io_json(json_file, user='boy', conversation_num=1):
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

def prepare_dataset(io_json_file, tokenizer):
    # データセットの準備
    with open(io_json_file) as f:
        io_data = json.load(f)
    print("データ数:", len(io_data))

    train_dataset = []
    val_dataset = []

    for i in range(len(io_data)):
        if i % 5 == 0:
            x = _tokenize(_generate_train_prompt(io_data[i]), tokenizer)
            val_dataset.append(x)
        else:
            x = _tokenize(_generate_train_prompt(io_data[i]), tokenizer)
            train_dataset.append(x)
    return train_dataset, val_dataset

def _generate_train_prompt(io_data):
    # プロンプトテンプレートの準備
    result = f"""{io_data["input"]}
    システム: {io_data["output"]}
    """
    # 改行→<NL>
    result = result.replace('\n', '<NL>')
    return result

# トークナイズ関数
def _tokenize(prompt, tokenizer):
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=settings.CUTOFF_LEN,
        padding=False,
    )
    return {
        "input_ids": result["input_ids"],
        "attention_mask": result["attention_mask"],
    }

