# ollama_agent_with_tools.py
from langchain_community.llms import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from tools import ShellCommandTool,OpenWebsite,LLMTool,ExceptTool
from speech_recognition import listen
def create_ollama_agent():
    llm = Ollama(model="llama3.2", base_url="http://localhost:11434")
    
    shell_tool = ShellCommandTool()
    website_tool = OpenWebsite()
    llm_tool = LLMTool()
    except_tool = ExceptTool()
    tools = [
        Tool(
            name="Execute Command",
            func=shell_tool.run,
            description="Search for an appropriate command useful for executing shell commands based on user query. Input should be a valid shell command."
        ),
        Tool(
            name="Open website",
            func=website_tool.run,
            description="Search for an appropriate website in the format of https://website.com. Input should be a valid URL."
        ),
        Tool(
            name="Know about topic",
            func=llm_tool.run,
            description="Use this tool to get any details pass sentence as query and get the result if you can't use any other tool. Input should be a sentence in question form."
        ),
        Tool(
            name="Ask Anything if not understood",
            func=except_tool.run,
            description="Use this tool if you don't konw anything. If you can't use any other tool. Not input needed."
        )
    ]
    
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=2
    )
    
    return agent

def main():
    
    agent = create_ollama_agent()
    
    print("Ollama Agent with Tools")
    print("Type 'exit' to quit")
    while True:
        user_input = listen()
        if user_input == None:
            continue
        
        if user_input.lower() == 'exit':
            break
        
        try:
            response = agent.run(user_input)
            print("\nAgent response:")
            print(response)
        except Exception as e:
            # Extract intermediate steps if available
            if hasattr(e, 'intermediate_steps'):
                steps = e.intermediate_steps
                print("Agent reached iteration limit, but here are the intermediate steps:")
                for i, step in enumerate(steps, 1):
                    print(f"\nStep {i}:")
                    print("  Action:", step[0])
                    print("  Observation:", step[1])
            else:
                print("Agent failed without intermediate steps:", str(e))

if __name__ == "__main__":
    main()