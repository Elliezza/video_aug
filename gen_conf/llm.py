from openai import OpenAI

client = OpenAI(api_key="46318b2ca8bc4f379eeee37700c8970f" ,
                base_url="http://modelhub.4pd.io/learnware/models/openai/4pd/api/v1")

def call_llm(prompt):

    res = client.chat.completions.create(
    model="public/waic-qwen2-72b-instruct-awq@main",
    messages=[{ "role": "user", "content": prompt }],
    temperature=0.5,
    max_tokens=4096,
    top_p=1,
    stop=None,
    )

    result = res.choices[0].message.content

    print(result)

    return result
