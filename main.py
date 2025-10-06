from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
#https://www.youtube.com/watch?v=XZdY15sHUa8
load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """"Useful for performing basic arithermitic calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    print("Tool has been called.")
    return f"Hello {name}, I hope you are well today"

@tool
def get_weather(city: str) -> str:
    """Useful for getting weather information for a specific city"""
    print("Tool has been called.")
    # In a real implementation, you would call a weather API here
    # For demo purposes, returning mock data
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Cloudy, 58°F", 
        "tokyo": "Rainy, 65°F",
        "paris": "Partly cloudy, 68°F"
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"The weather in {city.title()} is {weather_data[city_lower]}"
    else:
        return f"Sorry, I don't have weather data for {city}. Try New York, London, Tokyo, or Paris."

def main():
    model = ChatOpenAI(temperature=0)

    tools = [get_weather]
    agent_executer = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executer.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()



