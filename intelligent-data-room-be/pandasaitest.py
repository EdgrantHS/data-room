import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

llm = LiteLLM(model="gemini/gemini-2.5-flash-lite", api_key="censored")

pai.config.set({
    "llm": llm
})


# # Load sample dataset
# file_path = "data/Sample Superstore.csv"
# df = pai.read_csv(file_path)

# # Test query
# prompt = "What are the top 5 states by total sales?"
# print(f"Query: {prompt}")

# response = df.chat(prompt)
# print("\nResponse:")
# print(response)


# Hard data
data = {
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [21400000, 2830000, 2710000, 3860000, 2000000, 1390000, 1730000, 1390000, 5080000, 14140000],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.40, 7.23, 7.22, 5.87, 5.12]
}
df = pai.DataFrame(data)

# Test query
prompt = "Which are the 5 happiest countries?"

response = df.chat(prompt)
print(response)