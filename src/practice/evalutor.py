

from crewai.flow.flow import Flow, start, listen
from litellm import completion  
from dotenv import load_dotenv
import os

load_dotenv()

class WorkflowEvaluator(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")
    max_retries = 3  # Prevent infinite loops

    @start()
    def generator(self, retries=0):
        """ LLM Call Generator: Creates an initial response """
        prompt = "What is the capital of Pakistan?"
        response = self.generate_response(prompt)
        print(f"🎯 Generated Response (Attempt {retries}): {response} [Length: {len(response)}]")

        return {"response": response, "prompt": prompt, "retries": retries}
    
    @listen(generator)  
    def evaluator(self, data):
        """ LLM Call Evaluator: Checks response and provides feedback """
        response = data["response"]
        prompt = data["prompt"]
        retries = data["retries"]

        print(f"🔍 Evaluating Response (Attempt {retries + 1}): {response} [Length: {len(response)}]")

        if len(response) < 10:  
            # ✅ Accept if response is less than 50 characters
            print(f"✅ Accepted: {response}")
            facts = self.generate_response(f"Tell me interesting facts about {response}")
            print("📌 Final Output:", facts)
            return {"final_output": facts}
        
        if retries < self.max_retries:
            # ❌ Reject if response is too long
            )
            print(f"❌ Rejected (Too long). Retrying... [Retry {retries + 1}]")
            return self.generator(retries=retries + 1)  # 🔄 Loop back to generator
        
        print(f"⚠️ Maximum retries reached ({self.max_retries}). Accepting last response: {response}")
        return {"final_output": response}

    def generate_response(self, prompt):
        """ Calls LLM to generate a response """
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

def main():
    evaluator = WorkflowEvaluator()
    evaluator.kickoff()
    evaluator.plot()    
