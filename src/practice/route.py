from crewai.flow.flow import Flow , start , listen , router
from litellm import completion
from dotenv import load_dotenv  
import os
load_dotenv()

class RouterFlow(Flow):
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
        self.state["islamabad"] = "islamabad" in answer.lower()
        
        print(answer)   
        return answer
    
    @router(start)
    def router_start(self):
        if self.state.get("islamabad"):
            return "islamabad_flow"
        elif "lahore" in self.state.get("answer").lower():
            return "lahore_flow"
        elif "karachi" in self.state.get("answer").lower():
            return "karachi_flow"
        elif "quetta" in self.state.get("answer").lower():
            return "quetta_flow"
        elif "peshawar" in self.state.get("answer").lower():
            return "peshawar_flow"
        else:
            return "balochistan_flow"


    @listen("islamabad_flow")
    def listen_islamabad(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen("lahore_flow")
    def listen_lahore(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen("karachi_flow")
    def listen_karachi(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen("quetta_flow")
    def listen_quetta(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen("peshawar_flow")
    def listen_peshawar(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen("balochistan_flow")
    def listen_balochistan(self, answer):
        response = completion(
            model = self.model,
            api_key = self.api_key,
            messages=[{"role":"user","content":f"tell me the intresting facts about {answer}"}]
        )
        answer2 = response['choices'][0]['message']['content']
        print("Final Output:")
        print(answer2)
        return answer2
    
    @listen(listen_islamabad)
    @listen(listen_lahore)
    @listen(listen_karachi)
    @listen(listen_quetta)
    @listen(listen_peshawar)
    @listen(listen_balochistan)     
    def file_save(self, answer):
        with open("output.md", "w") as file:
            file.write(answer)
        return answer

    # @listen("islamabad_flow", "lahore_flow", "karachi_flow", "quetta_flow", "peshawar_flow", "balochistan_flow")
    # def file_save(self, answer):
    #     with open("output.txt", "w") as file:
    #         file.write(answer)
    #     print("File Saved")

    
def main():
    flow = RouterFlow()
    flow.kickoff()
    flow.plot()