from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

tokenizer = None
model = None


def get_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    return tokenizer, model


def explain_topic(topic: str) -> str:
    if not topic.strip():
        return "Please enter a topic to explain."

    try:
        tokenizer, model = get_model()

        prompt = f"""
Explain the following educational topic clearly for a student.

Topic:
{topic}

Give:
1. Simple definition
2. Main concepts
3. How it works
4. A simple example
5. Short summary

Use simple and easy-to-understand language.
"""

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=False
            )

        result = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return result.strip()

    except Exception as e:
        return f"Error in Explanation: {str(e)}"