import configparser
from transformers import AutoTokenizer


conf = configparser.ConfigParser()
conf.read('settings.ini')

boy_name = conf['dataset']['boy_name']
girl_name = conf['dataset']['girl_name']

# モデル基本情報
model_name = 'rinna/japanese-gpt-neox-3.6b-instruction-sft-v2'
peft_name = 'lorasft2-rinna-3.6b'
output_dir = 'lorasft2-rinna-3.6b-results'

# トークナイザーの準備
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

CUTOFF_LEN = 256  # コンテキスト長
VAL_SET_SIZE = 1000

# model
eval_steps = 200
save_steps = 200
logging_steps = 20
