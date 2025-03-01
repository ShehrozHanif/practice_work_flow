from crewai.flow.flow import Flow , start , listen , and_
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()



class OrchestratorFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    api_key = os.getenv("GEMINI_API_KEY")

    @start()
    def orchestrate(self):
        """Start the process by generating the initial input"""
        prompt = "Generate a futuristic idea for a new AI product."
        print("Orchestrator starting with prompt:", prompt)
        return prompt

    @listen(orchestrate)
    def llm_call_1(self, input_text):
        """First LLM call to generate an initial idea"""
        response = completion(
            model=self.model,
            api_key=self.api_key, 
            messages=[{"role": "user", "content": input_text}])
        idea = response["choices"][0]["message"]["content"].strip()
        self.state["idea"] = idea
        print("LLM Call 1 Output:", idea)
        return idea

    @listen(orchestrate)
    def llm_call_2(self, input_text):
        """Second LLM call to refine the idea"""
        response = completion(
            model=self.model,
            api_key=self.api_key, 
            messages=[{"role": "user", "content": f"Refine this idea: {input_text}"}])
        refined_idea = response["choices"][0]["message"]["content"].strip()
        self.state["refined_idea"] = refined_idea
        print("LLM Call 2 Output:", refined_idea)
        return refined_idea

    @listen(orchestrate)
    def llm_call_3(self, input_text):
        """Third LLM call to generate a potential use case"""
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": f"Give a use case for this idea: {input_text}"}])
        use_case = response["choices"][0]["message"]["content"].strip()
        self.state["use_case"] = use_case
        print("LLM Call 3 Output:", use_case)
        return use_case

    @listen(and_(llm_call_1, llm_call_2, llm_call_3))


    def synthesizer(self):
        """Synthesizes all outputs into a final response"""

        # idea, refined_idea, use_case = outputs
        idea = self.state.get("idea")
        refined_idea = self.state.get("refined_idea")
        use_case = self.state.get("use_case")

        synthesized_result = (
            f"Original Idea: {idea}\n"
            f"Refined Idea: {refined_idea}\n"
            f"Use Case: {use_case}"
        )
        print("Final Synthesized Output:\n", synthesized_result)
        return synthesized_result
    
    @listen(synthesizer)
    def file_output(self, final_output):
        """Write the final output to a file"""
        with open("final_output.md", "w") as file:
            file.write(final_output)
        print("Final output written to 'final_output.md'")
        return final_output

def main():
    flow = OrchestratorFlow()
    final_output = flow.kickoff()
    print("\nFinal Output of the Flow:\n", final_output)
    flow.plot()
    