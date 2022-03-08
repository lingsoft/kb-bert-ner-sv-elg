from transformers import pipeline

ner = pipeline(
    task='ner',
    model='KB/bert-base-swedish-cased-ner',
    tokenizer='KB/bert-base-swedish-cased-ner',
    grouped_entities=True,
)
# Save pipeline
path = 'local_kb_bert_ner'
ner.save_pretrained(path)
