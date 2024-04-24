from transformers import AutoModelForCausalLM
from mistral_common.protocol.instruct.messages import (
    AssistantMessage,
    UserMessage,
)
from mistral_common.protocol.instruct.tool_calls import (
    Tool,
    Function,
)
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.tokens.instruct.normalize import ChatCompletionRequest

device = "cuda" # the device to load the model onto

tokenizer_v3 = MistralTokenizer.v3()

mistral_query = ChatCompletionRequest(
    tools=[
        Tool(
            function=Function(
                name="get_current_weather",
                description="Get the current weather",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "format": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the users location.",
                        },
                    },
                    "required": ["location", "format"],
                },
            )
        )
    ],
    messages=[
        UserMessage(content="What's the weather like today in Paris"),
    ],
    model="test",
)

encodeds = tokenizer_v3.encode_chat_completion(mistral_query).tokens
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-Instruct-v0.1")
model_inputs = encodeds.to(device)
model.to(device)

generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
sp_tokenizer = tokenizer_v3.instruct_tokenizer.tokenizer
decoded = sp_tokenizer.decode(generated_ids[0])
print(decoded)
