import os
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
from pandasai.core.response.chart import ChartResponse
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

llm = LiteLLM(model="gemini/gemini-2.5-flash-lite", api_key=api_key)
pai.config.set({"llm": llm})

data = {
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [21400000, 2830000, 2710000, 3860000, 2000000, 1390000, 1730000, 1390000, 5080000, 14140000],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.40, 7.23, 7.22, 5.87, 5.12]
}
df = pai.DataFrame(data)

# Test query
prompt = "Graph countries by happiness_index"

print("Prompt:", prompt)

response = df.chat(prompt)
print(f"Response type: {type(response)}")

if isinstance(response, ChartResponse):
    base64_img = response.get_base64_image()
    print(f"Base64 image length: {len(base64_img)}")
    print(f"base64 image:\ndata:image/png;base64,{base64_img}")
else:
    print("Response is not a chart.")
    print(response)