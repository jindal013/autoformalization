from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json

torch.manual_seed(30)

model_id = "deepseek-ai/DeepSeek-Prover-V2-7B"  # or DeepSeek-Prover-V2-671B
print('loading tokenizer...')
tokenizer = AutoTokenizer.from_pretrained(model_id)
print('tokenizer loaded!')
# formal_statement = """The fundamental group of the circle is isomorphic to the integers""".strip()

prompt = """
Please formalize the following mathematical statement in Lean 4: The torus is a topological space whose fundamental group is isomorphic to the product of two copies of the integers Provide only the Lean 4 code without any explanations:
""".strip()

chat = [
    {"role": "user", "content": prompt},
]
print('reached here!')

model = AutoModelForCausalLM.from_pretrained(
    model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
)
inputs = tokenizer.apply_chat_template(
    chat, tokenize=True, add_generation_prompt=True, return_tensors="pt"
).to(model.device)

import time

start = time.time()
outputs = model.generate(inputs, max_new_tokens=8192)
decoded = tokenizer.batch_decode(outputs)
print(decoded)
print(time.time() - start)

# Write output to output.json
output_dict = {
    "query": "The fundamental group of the circle is isomorphic to the integers",
    "lean_code": decoded[0] if isinstance(decoded, list) and len(decoded) > 0 else "",
}
with open("output.json", "w") as f:
    json.dump(output_dict, f, indent=2)
