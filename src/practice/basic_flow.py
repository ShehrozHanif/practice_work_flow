from crewai.flow.flow import Flow , start , listen
from litellm import completion 
from dotenv import load_dotenv
import os               
load_dotenv()


class BasicFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def start(self):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":"what is the capital of pakistan"}]
        )
        answer = response["choices"][0]["message"]["content"]
        print(answer)   
        return answer
    
    @listen(start)
    def listen_start(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
        



def main():
    flow = BasicFlow()
    flow.kickoff()
