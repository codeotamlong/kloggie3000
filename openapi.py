from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

ret = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "tự hưng hôm nay chán quá, trời lạnh ăn lẩu thì ngon",
        }
    ],
    model="gpt-3.5-turbo",
)

print (ret.choices[0].message.content)