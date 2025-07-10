from langchain.agents import create_tool_calling_agent, AgentExecutor, Tool
from langchain_openai import ChatOpenAI
from tools.smoldocling import smoldocling_tool
from tools.gemini import gemini_tool
from tools.gpt_extractor import extractor_tool
from tools.evaluation import evaluate_tool
from tools.retry import retry_tool
from tools.prompt_applier import apply_prompt_tool
from tools.conversation import conversation_tool
from tools.final_output import final_output_tool
from utils.prompts import SUPERVISOR_SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Prompt template with placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", SUPERVISOR_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_prompt}, {file_content}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [
    Tool(name="smoldocling", func=smoldocling_tool,
         description="Extract structure."),
    Tool(name="gemini", func=gemini_tool, description="Extract ALL visual Elements in files."),
#     Tool(name="extractor", func=extractor_tool, description="Extract content."),
#     Tool(name="evaluate", func=evaluate_tool, description="Evaluate outputs."),
#     Tool(name="retry", func=retry_tool, description="Retry after feedback."),
#     Tool(name="apply_prompt", func=apply_prompt_tool,
#          description="Apply user prompt."),
#     Tool(name="conversation", func=conversation_tool,
#          description="Handle prompt-only case."),
#     Tool(name="final_output", func=final_output_tool,
#          description="Produce final doc."),
]

# Create the tool-calling agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

# Wrap in executor for proper control looping
supervisor_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)

print(prompt)
