from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.toolkits import MathToolkit, SearchToolkit
from camel.agents import ChatAgent
# Define the model, here in this case we use gpt-4o-mini
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O_MINI,
    model_config_dict=ChatGPTConfig(stream=True).as_dict(), # [Optional] the config for model
)


sys_msg = 'Bạn là chuyên gia tài chính có nhiều kinh nghiệm thương trường.'
agent = ChatAgent(
    system_message=sys_msg,
    tools = [
        # *MathToolkit().get_tools(),
        # *SearchToolkit().get_tools(),
    ],
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
# Define a user message
usr_msg = 'so sánh cổ phiếu và crypto'

# Sending the message to the agent
response = agent.step(usr_msg)
# stream =agent._handle_stream_response(usr_msg, stream=True)
for event in response:
    print(event)
    # print(event.msgs[0],end="", flush=True)
# print(response.msgs[0].content)
# Check the response (just for illustrative purpose)

# print(agent.memory.get_context())