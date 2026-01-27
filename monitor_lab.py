import os
from openai import OpenAI
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Register the Arize server
tracer_provider = register(
    project_name="monitor_lab",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument the OpenAI client
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
# Monkey patching

# Create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():

    # Make a request to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain the difference between a Trace and a Span in 2 sentences."}
        ]
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()