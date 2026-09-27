import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Explain in one sentence what makes a YouTube moment interesting for a short video."
        }
    ]
)

print(response["message"]["content"])