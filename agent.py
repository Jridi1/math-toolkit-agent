#the react agent

import json
import math

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()  # loads GROQ_API_KEY from .env
#data validation
class NumbersInput(BaseModel):
    numbers: list[float] = Field(
        min_length=2,
        description="Two or more numbers, for example: [2, 3.5, -4]"
    )

@tool(args_schema = NumbersInput)
def add_numbers(numbers: list[float]) -> dict[str, float | str]:
    """
    Add numbers together and return their sum.
    Use this tool when the user wants to add, sum or total two or more numbers.

    Args:
        numbers (list[float]): The numbers to add.

    Returns:
        (dict[str, float | str]): A dict with the key "result" holding the sum.
    """
    return {"result": sum(numbers)}


@tool(args_schema=NumbersInput)
def subtract_numbers(numbers: list[float]) -> dict[str, float | str]:
    """
    Subtract numbers from the first one, in order.
    Use this tool when the user wants to subtract or take away numbers.
    For [10, 3, 2] the result is 10 minus 3 minus 2, which is 5.

    Args:
        numbers (list[float]): The first number, followed by the numbers to subtract.

    Returns:
        (dict[str, float | str]): A dict with the key "result" holding the difference.
    """
    return {"result": numbers[0] - sum(numbers[1:])}

@tool(args_schema=NumbersInput)
def multiply_numbers(numbers: list[float]) -> dict[str, float | str]:
    """
    Multiply numbers together and return the product.
    Use this tool when the user wants to multiply two or more numbers.

    Args:
        numbers (list[float]): The numbers to multiply.

    Returns:
        (dict[str, float | str]): A dict with the key "result" holding the product.
    """
    return {"result": math.prod(numbers)}

@tool(args_schema=NumbersInput)
def divide_numbers(numbers: list[float]) -> dict[str, float | str]:
    """
    Divide the first number by the others, in order.
    Use this tool when the user wants to divide numbers.
    For [100, 5, 2] the result is 100 divided by 5 divided by 2, which is 10.

    Args:
        numbers (list[float]): The dividend, followed by one or more divisors.

    Returns:
        (dict[str, float | str]): A dict with the key "result" holding the quotient,
        or the key "error" with a short message if a divisor is zero.
    """
    result = numbers[0]
    for divisor in numbers[1:]:
        if divisor == 0:
            return {"error": "Division by zero is not allowed."}
        result /= divisor
    return {"result": result}

tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

tool_map = {t.name: t for t in tools}

#2. LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
    )
#3. bind the tools
llm_with_tools = llm.bind_tools(tools)

# 4. Output format: the number comes from the tool, the text from the LLM
class Calculation(BaseModel):
    tool: str
    inputs: list[float]
    output: dict

class MathAnswer(BaseModel):
    answer: str
    calculations: list[Calculation]

# 5. Prompt and loop
SYSTEM_PROMPT = """You are a math assistant.
Rules:
1. For every calculation you must call a tool. Never calculate in your head.
2. For several operations, call the tools one after another and reuse earlier results.
3. If a tool returns an error, explain it to the user in one short sentence.
4. If the question is not about math, say that you only help with math.
5. Keep the final answer short."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{input}"),
 ])

def run_agent(question: str, max_steps: int = 5) -> MathAnswer:
    messages = prompt.format_messages(input=question)
    calculations: list[Calculation] = []

    for _ in range(max_steps):
        ai_message = llm_with_tools.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            return MathAnswer(answer=ai_message.content, calculations=calculations)

        for call in ai_message.tool_calls:
            try:
                result = tool_map[call["name"]].invoke(call["args"])
            except Exception as e:  # bad arguments or unknown tool
                result = {"error": str(e)}

            calculations.append(Calculation(
                tool=call["name"],
                inputs=call["args"].get("numbers", []),
                output=result,
            ))
            messages.append(ToolMessage(content=json.dumps(result), tool_call_id=call["id"]))

    return MathAnswer(answer="Stopped: too many steps.", calculations=calculations)


if __name__ == "__main__":
    question = input("Your question: ")
    response = run_agent(question)
    print(response.model_dump_json(indent=2))