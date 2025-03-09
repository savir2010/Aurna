from transformers import pipeline

from huggingface_hub import login

login("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")

pipe = pipeline("image-generation", model="dalle-mini/dalle-mini")

# Generate an image from a prompt
prompt = "A cyberpunk cat wearing sunglasses"
image = pipe(prompt)[0]["image"]

# Display the image
image.show()