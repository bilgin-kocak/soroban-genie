import streamlit as st
from anthropic import Anthropic
import re
import os

# Replace with your actual API key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

def generate_smart_contract(user_prompt):
    prompt_template = f"""
    You are an AI assistant specialized in generating Soroban smart contracts. Create a Rust smart contract for the Soroban platform based on the following description. Only provide the Rust code for the contract, without any explanations.

    Contract description: {user_prompt}

    Please ensure the contract follows Soroban best practices, includes appropriate error handling, and is optimized for efficiency. The contract should be complete and ready for compilation.

    Generate the Soroban smart contract code:
    """

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            # {"role": "system", "content": "You are a Soroban smart contract expert."},
            {"role": "user", "content": prompt_template}
        ]
    )
    
    return response.content[0].text


def extract_rust_code(text):
    # Regular expression to match Rust code blocks
    pattern = r'```rust\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    return text  # Return the original text if no Rust code block is found

# Streamlit app
st.set_page_config(page_title="SorobanGenie", page_icon="🧞", layout="wide")

# Landing page
st.title("🧞 SorobanGenie")
st.markdown("""
Welcome to SorobanGenie, your AI-powered assistant for creating Soroban smart contracts!

### Key Features:
- **AI-Powered Contract Generation**: Transform natural language into Soroban-compatible code
- **Streamlined Development**: Save time and reduce errors in smart contract creation
- **Accessibility**: Create blockchain solutions without extensive coding knowledge

Get started by describing your smart contract below!
""")

# Code generation section
st.header("Generate Your Soroban Smart Contract")
user_prompt = st.text_area("Describe your smart contract:", height=150,
                           value="Create a Soroban smart contract that stores and retrieves a greeting message. The contract should have two functions: one to set the greeting and another to get the greeting. The initial greeting should be 'Hello, World!")

if st.button("Generate Contract"):
    if user_prompt:
        with st.spinner("Generating your smart contract..."):
            generated_response = generate_smart_contract(user_prompt)
            generated_code = extract_rust_code(generated_response)

            # Add the markdown header
            st.markdown("#### SorobanGenie: Here's the Soroban smart contract code based on your description:")
            st.code(generated_code, language="rust", line_numbers=True)
    else:
        st.warning("Please provide a description for your smart contract.")

# Add a footer
st.markdown("---")
st.markdown("© 2024 SorobanGenie. All rights reserved.")