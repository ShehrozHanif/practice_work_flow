from crewai.flow.flow import Flow , start , listen , and_
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()



class AndAggregationFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def generate_slogan(self):
        # This task generates a creative slogan.
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": "Generate a five creative slogan for a futuristic brand."
            }]
        )
        slogan = response["choices"][0]["message"]["content"].strip()
        print("Slogan generated:", slogan)
        self.state["slogan"] = slogan  
        return slogan

    @start()
    def generate_tagline(self):
        # This task generates a creative tagline.
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{
                "role": "user",
                "content": "Generate a five creative tagline for a futuristic brand."
            }]
        )
        tagline = response["choices"][0]["message"]["content"].strip()
        print("Tagline generated:", tagline)
        self.state["tagline"] = tagline  
        
        return tagline
    
 
    @listen(and_(generate_slogan, generate_tagline))
    def combine_outputs(self):  # <-- FIX: Separate arguments
        # The `and_` decorator ensures this method is called only when both tasks complete.
        stored_slogan = self.state.get("slogan")
        stored_tagline = self.state.get("tagline")
        combined = f"Combined Output: Slogan - '{stored_slogan}' | Tagline - '{stored_tagline}'"
        print("Aggregated Combined Output:", combined)
        return combined

def main():
    flow = AndAggregationFlow()
    final_output = flow.kickoff()
    flow.plot()
    print("Final Output of the Flow:")
    print(final_output)
