# llm.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

_pipeline = None
_current_model = None

def get_llm(model_type="default"):
    global _pipeline, _current_model
    model_id = "google/gemma-3-1b-it" if model_type == "default" else "Qwen/Qwen2.5-3B-Instruct"

    if _current_model == model_id and _pipeline is not None:
        return _pipeline

    if _pipeline is not None:
        print(f"Unloading {_current_model}...")
        del _pipeline
        torch.cuda.empty_cache()

    print(f"Loading {model_id}...")

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        clean_up_tokenization_spaces=False
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="cuda"
    )

    _pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
    )
    _current_model = model_id
    print("Model loaded.")
    return _pipeline


def generate(prompt: str, model_type="default") -> str:
    pipe = get_llm(model_type)
    messages = [{"role": "user", "content": prompt}]
    output = pipe(messages)
    return output[0]["generated_text"][-1]["content"].strip()


if __name__ == "__main__":
    response = generate("What is a transformer in one sentence?", model_type="default")
    print("Default model:", response)

    response = generate("What is attention mechanism in one sentence?", model_type="commentary")
    print("Commentary model:", response)
    print("llm.py OK")