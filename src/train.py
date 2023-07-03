from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, prepare_model_for_int8_training, TaskType
import transformers

import settings


def load_model(model_name, train_dataset, val_dataset):
    # モデルの準備
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_8bit=True,
        device_map="auto",
    )

    # LoRAのパラメータ
    lora_config = LoraConfig(
        r= 8,
        lora_alpha=16,
        target_modules=["query_key_value"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # モデルの前処理
    model = prepare_model_for_int8_training(model)

    # LoRAモデルの準備
    model = get_peft_model(model, lora_config)

    # 学習可能パラメータの確認
    model.print_trainable_parameters()

    eval_steps = settings.eval_steps
    save_steps = settings.save_steps
    logging_steps = settings.logging_steps

    # トレーナーの準備
    trainer = transformers.Trainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=transformers.TrainingArguments(
            num_train_epochs=3,
            learning_rate=3e-4,
            logging_steps=logging_steps,
            evaluation_strategy="steps",
            save_strategy="steps",
            eval_steps=eval_steps,
            save_steps=save_steps,
            output_dir=settings.output_dir,
            save_total_limit=3,
            push_to_hub=False,
            auto_find_batch_size=True
        ),
        data_collator=transformers.DataCollatorForLanguageModeling(settings.tokenizer, mlm=False),
    )
    return model, trainer

def my_train(model, trainer):
    # 学習の実行
    model.config.use_cache = False
    trainer.train()
    model.config.use_cache = True

    # LoRAモデルの保存
    trainer.model.save_pretrained(settings.peft_name)