from datasets import load_dataset
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
import torch

dataset = load_dataset("Teklia/IAM-line")
train_ds = dataset["train"]
val_ds = dataset["validation"]

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def preprocess_batch(batch):
    images = [img.convert("RGB") for img in batch["image"]]
    pixel_values = processor(images, return_tensors="pt").pixel_values
    labels = processor.tokenizer(
        batch["text"], padding="max_length", max_length=128, truncation=True
    ).input_ids
    labels = [[l if l != processor.tokenizer.pad_token_id else -100 for l in label] for label in labels]
    batch["pixel_values"] = pixel_values
    batch["labels"] = labels
    return batch

train_ds = train_ds.map(preprocess_batch, batched=True)
val_ds = val_ds.map(preprocess_batch, batched=True)

training_args = Seq2SeqTrainingArguments(
    output_dir="./trocr-finetuned",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    fp16=torch.cuda.is_available(),
    logging_steps=50,
    save_steps=500,
    eval_strategy="steps",
    eval_steps=500,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
)

if __name__ == "__main__":
    trainer.train()
    model.save_pretrained("./trocr-finetuned")
    processor.save_pretrained("./trocr-finetuned")