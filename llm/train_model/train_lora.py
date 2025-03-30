import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

# 1️⃣ Chọn mô hình pre-trained
MODEL_NAME = "meta-llama/Llama-2-7b-hf"  # Hoặc "mistralai/Mistral-7B-v0.1"
TOKENIZER_NAME = MODEL_NAME

# 2️⃣ Load mô hình và tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_8bit=True,  # Sử dụng 8-bit để tiết kiệm VRAM
    device_map="auto"
)

# 3️⃣ Cấu hình LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, # Dùng cho LLM (GPT-style models)
    r=16,  # Rank của LoRA (giá trị nhỏ giúp giảm số tham số)
    lora_alpha=32,  # Hệ số alpha (càng cao, càng có tác động)
    lora_dropout=0.05,  # Dropout để tránh overfitting
    target_modules=["q_proj", "v_proj"]  # Áp dụng LoRA cho self-attention layers
)

# 4️⃣ Áp dụng LoRA lên mô hình
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 5️⃣ Load dữ liệu huấn luyện
dataset = load_dataset("Abirate/english_quotes", split="train[:1%]")  # Chỉ lấy 1% data

def tokenize_function(examples):
    return tokenizer(examples["quote"], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 6️⃣ Cấu hình huấn luyện
training_args = TrainingArguments(
    output_dir="./lora_llm",
    per_device_train_batch_size=4,  # Tùy chỉnh theo VRAM
    gradient_accumulation_steps=16,  # Tăng batch size hiệu quả
    optim="adamw_bnb_8bit",  # Dùng optim 8-bit
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    num_train_epochs=3,
    fp16=True,  # Dùng mixed precision để tiết kiệm bộ nhớ
    report_to="none"
)

# 7️⃣ Huấn luyện mô hình
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets
)
trainer.train()

# 8️⃣ Lưu LoRA adapters (Không lưu toàn bộ mô hình để tiết kiệm dung lượng)
model.save_pretrained("lora_model")
