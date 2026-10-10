# Math Toolkit Agent

A tool calling math agent built with LangChain and Groq. You ask a question in plain English, the model picks the right math tool, your code runs it, and you get back a short answer plus the exact calculations that were executed.

The number never comes from the LLM. It comes from the tool output, so every result can be verified.

## Features

* Four tools: add, subtract, multiply and divide, each accepting two or more numbers
* Input validation with Pydantic, so bad input is rejected before any tool runs
* Division by zero handled with a clear error instead of a crash
* Multi step questions, for example "add 2 and 3, then multiply the result by 4"
* Structured output: a short answer from the LLM and a calculation trace recorded by the code
* Step limit to stop the agent from looping forever
* Unit tests for every tool

## How it works

1. The user types a question in the terminal.
2. The LLM reads the question and decides which tool to call, with which numbers.
3. The code runs the tool and sends the result back to the LLM.
4. The LLM repeats this if more steps are needed, then writes the final answer.
5. The program prints the answer and the list of calculations as JSON.

## Tech stack

Python, LangChain, Groq (`openai/gpt-oss-120b`), Pydantic, pytest

## Setup

1. Clone the repository

```bash
git clone https://github.com/Jridi1/math-toolkit-agent.git
cd math-toolkit-agent
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Add your Groq API key. Copy the example file and put your own key inside it. You can get a free key at console.groq.com.

```bash
cp .env.example .env
```

Then edit `.env`:

```
GROQ_API_KEY=your_key_here
```

## Usage

```bash
python agent.py
```

Example session:

```
Your question: Add 2 and 3, then multiply the result by 4
```

```json
Your question: add 2 and 3, then multiply the result by 4
{
  "answer": "20.0",
  "calculations": [
    {
      "tool": "add_numbers",
      "inputs": [
        2.0,
        3.0
      ],
      "output": {
        "result": 5.0
      }
    },
    {
      "tool": "multiply_numbers",
      "inputs": [
        5.0,
        4.0
      ],
      "output": {
        "result": 20.0
      }
    }
  ]
}
```

The exact wording of `answer` can change between runs. The `calculations` list is produced by the code, so it is exact.

## Tests

The tool tests do not call the API, so they are fast and free:

```bash
pytest test_tools.py -v
```

## Project structure

* `agent.py`: tools, LLM setup, agent loop and terminal entry point
* `test_tools.py`: unit tests for the four tools
* `requirements.txt`: Python dependencies
* `.env.example`: template for your API key

## Limitations and next steps

* Only basic operations for now
* Planned: power and square root, an expression solver with SymPy, statistics tools, unit conversion and chat memory
* Planned: a simple web interface

## Author

Abderrahim Jridi
