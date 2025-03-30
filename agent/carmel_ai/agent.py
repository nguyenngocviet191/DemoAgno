from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.toolkits import MathToolkit, SearchToolkit
sys_msg = 'You are a Yugioh card trader.'
# Define the model, here in this case we use gpt-4o-mini
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O_MINI,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
)

from camel.agents import ChatAgent
agent = ChatAgent(
    system_message=sys_msg,
    tools = [
        *MathToolkit().get_tools(),
        *SearchToolkit().get_tools(),
    ],
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
# Define a user message
usr_msg = 'tell me top 10 expensive yugioh cards'

# Sending the message to the agent
response = agent.step(usr_msg)

# Check the response (just for illustrative purpose)
print(response.msgs[0].content)