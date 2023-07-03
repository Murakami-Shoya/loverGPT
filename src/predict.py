import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import settings

model = AutoModelForCausalLM.from_pretrained(
    settings.model_name,
    load_in_8bit=True,
    device_map="auto",
)

# LoRAモデルの準備
model = PeftModel.from_pretrained(
    model,
    settings.peft_name,
    device_map="auto"
)

# # 評価モード
# model.eval()


# # テキスト生成関数の定義
# def generate(instruction, input=None, maxTokens=256) -> str:
#     # 推論
#     prompt = _generate_eval_prompt(instruction)
#     input_ids = settings.tokenizer(prompt,
#                           return_tensors="pt",
#                           truncation=True,
#                           add_special_tokens=False).input_ids.cuda()
#     outputs = model.generate(
#         input_ids=input_ids,
#         max_new_tokens=maxTokens,
#         do_sample=True,
#         temperature=0.7,
#         top_p=0.75,
#         top_k=40,
#         no_repeat_ngram_size=2,
#     )
#     outputs = outputs[0].tolist()
#     # print(tokenizer.decode(outputs))

#     # EOSトークンにヒットしたらデコード完了
#     if settings.tokenizer.eos_token_id in outputs:
#         eos_index = outputs.index(settings.tokenizer.eos_token_id)
#         decoded = settings.tokenizer.decode(outputs[:eos_index])
#         output = decoded.replace("<NL>", "\n")
#         # output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
#         return output

def generate_chat(input, model):
    if torch.cuda.is_available():
        model = model.to("cuda")

    prompt = _generate_eval_prompt(input)
    token_ids = settings.tokenizer.encode(
                            prompt, 
                            add_special_tokens=False, 
                            return_tensors="pt")

    # input_ids = settings.tokenizer(prompt,
    #                       return_tensors="pt",
    #                       truncation=True,
    #                       add_special_tokens=False).input_ids.cuda()

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=token_ids.to(model.device),
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            repetition_penalty=1.1,
            pad_token_id=settings.tokenizer.pad_token_id,
            bos_token_id=settings.tokenizer.bos_token_id,
            eos_token_id=settings.tokenizer.eos_token_id
            
        )

    output = settings.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
    output = output.replace("<NL>", "\n")
    return output

def _generate_eval_prompt(txt):
    # プロンプトテンプレートの準備
    result = f'ユーザ: {txt}システム: '
    # 改行→<NL>
    result = result.replace('\n', '<NL>')
    return result

while(1):
    user_input = input('ユーザ： ')
    print(generate_chat(user_input, model))