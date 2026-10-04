from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
reply = client.chat.completions.create(
    model="pharmacy-assistant",
    messages=[{"role": "system", "content": "You are a pirate. Answer in pirate speech."},
              {"role": "user", "content": "What is the price of Amoxicillin (AMOX02)?"}])
print(reply.choices[0].message.content)