from crewai.flow.flow import Flow , start , listen , or_
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()


class OrFlow(Flow):
    model1 = "gemini/gemini-1.5-flash"
    model2 = "gemini/gemini-2.0-flash"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def start1(self):
        response = completion(
            model = self.model1,
            api_key = self.api_key,
            messages=[{"role":"user","content":"name the best food dishes in pakistan"}]
        )
        answer = response["choices"][0]["message"]["content"]
        self.state["islamabad"] = "islamabad" in answer.lower()
        print(answer)   
        return answer
    
    @start() 
    def start2(self):
        response = completion(
            model = self.model2,
            api_key = self.api_key,
            messages=[{"role":"user","content":"name the best food dishes in pakistan"}]
        )
        answer = response["choices"][0]["message"]["content"]
        self.state["islamabad"] = "islamabad" in answer.lower()
        print(answer)   
        return answer
    
    @listen(or_(start1,start2))
    def listen_start(self, answer):
        response = completion(
            model = self.model1,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen(listen_start)
    def file_Save(self, answer):
        with open("output.txt", "w") as file:
            file.write(answer)
        return answer
    




def main():
    flow = OrFlow()
    flow.kickoff()
    flow.plot()
