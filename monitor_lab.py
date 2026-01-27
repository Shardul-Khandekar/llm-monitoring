import os
import time
from openai import OpenAI
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from dotenv import load_dotenv

# Load enviornment file
load_dotenv()

# Register the Arize server
tracer_provider = register(
    project_name="monitor_lab",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument the OpenAI client
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
# Monkey patching

# Create a tracer for manual spans
tracer = trace.get_tracer("monitor_lab_tracer")

# Create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_input(text):
    # Consider the function takes care of heavy preprocessing
    with tracer.start_as_current_span("clean_input_step") as span:
        print("Cleaning input")
        time.sleep(0.5)
        # Use span to set a manual attribute
        span.set_attribute("input_length", len(text))
        return text.strip().lower()
    
def run_workflow(user_query):
    # Create a parent span for the entire workflow
    with tracer.start_as_current_span("run_workflow") as span:
        
        cleaned_query = clean_input(user_query)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": cleaned_query}
            ]
        )
        return response.choices[0].message.content

def main():
    user_query = "   What is the capital of France? "
    answer = run_workflow(user_query)
    print("Answer:", answer)

if __name__ == "__main__":
    main()