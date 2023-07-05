# TODO 会話の長さをランダムで変更
# TODO 「おやすみ」で会話区切って意味的なまとまりを作る
# TODO boyかgirlかを切り替えられるようにする

import json
import settings

def create_io_json(json_file, user='boy'):
    """
    input, instruction, output の形式にする
    """
    io_json = []

    with open(json_file) as f:
        chat_json = json.load(f)

    speaker = lambda _i: '### ユーザ' if chat_json[_i]['speaker'] == user else '### 恋人'
    for i in range(0, len(chat_json), 2):
        try:
            if (speaker(i)!='### ユーザ'):
                i += 1
            # instruction = '\n'.join([f"{speaker(j)}: {chat_json[j]['text']}" for j in range(i, i+conversation_num)])
            instruction = f"{speaker(i)}: {chat_json[i]['text']}"
            input = f"{speaker(i-1)}: {chat_json[i-1]['text']}"
            output = f"{speaker(i+1)}: {chat_json[i+1]['text']}"
            dict = {"instruction":instruction,
                    "input": input,
                    "output": output}
            io_json.append(dict)
        except IndexError as e:
            print(e)
            break
    # print(io_json[:2], io_json[-2:])
    with open('io_dataset.json', 'w') as f:
        json.dump(io_json, f, indent=2)

    print(_generate_train_prompt(io_json[0]))
    print(_generate_train_prompt(io_json[-1]))

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
    result = f"""以下は、ユーザと恋人とのチャットです。
    {io_data["input"]}
    {io_data["instruction"]}
    {io_data["output"]}
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

# create_io_json('/code/chat_dataset.json')

# with open('/code/io_dataset.json') as f:
#     io_data = json.load(f)
#     # print(io_data[0])
#     print(_generate_train_prompt(io_data[-1]))
