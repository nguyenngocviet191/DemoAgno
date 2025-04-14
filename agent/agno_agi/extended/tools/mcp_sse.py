from functools import partial
from typing import Optional
from uuid import uuid4
import aiohttp
import asyncio

from agno.agent import Agent
from agno.media import ImageArtifact
from agno.tools import Toolkit
from agno.tools.function import Function
from agno.utils.log import log_debug, logger


class MCPToolsSSE(Toolkit):
    """
    A toolkit for integrating Model Context Protocol (MCP) servers with SSE (Server-Sent Events).
    This allows agents to access tools, resources, and prompts exposed by MCP servers in real-time.
    """

    def __init__(
        self,
        sse_url: str,
        include_tools: Optional[list[str]] = None,
        exclude_tools: Optional[list[str]] = None,
    ):
        """
        Initialize the MCP toolkit with SSE.

        Args:
            sse_url: The URL of the SSE server.
            include_tools: Optional list of tool names to include (if None, includes all).
            exclude_tools: Optional list of tool names to exclude (if None, excludes none).
        """
        super().__init__(name="MCPToolkitSSE")
        self.sse_url = sse_url
        self.include_tools = include_tools
        self.exclude_tools = exclude_tools or []
        self.available_tools = []
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the MCP toolkit by getting available tools from the SSE server."""
        if self._initialized: # Already initialized
            return

        try:
            log_debug(f"Try to init Tookit")
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.sse_url}/list-tools") as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch tools: {response.status}")
                    tools_data = await response.json()
                    self.available_tools = tools_data.get("tools", [])
            log_debug(f"Available tools: {self.available_tools}")

            # Filter tools based on include/exclude lists
            filtered_tools = []
            for tool in self.available_tools:
                if tool["name"] in self.exclude_tools:
                    continue
                if self.include_tools is None or tool["name"] in self.include_tools:
                    filtered_tools.append(tool)

            # Register the tools with the toolkit
            for tool in filtered_tools:
                try:
                    # Get an entrypoint for the tool
                    entrypoint = self.get_entrypoint_for_tool(tool)

                    # Create a Function for the tool
                    f = Function(
                        name=tool["name"],
                        description=tool["description"],
                        parameters=tool.get("inputSchema", {}),
                        entrypoint=entrypoint,
                        skip_entrypoint_processing=True,
                    )

                    # Register the Function with the toolkit
                    self.functions[f.name] = f
                    log_debug(f"Function: {f.name} registered with {self.name}")
                except Exception as e:
                    logger.error(f"Failed to register tool {tool['name']}: {e}")

            log_debug(f"{self.name} initialized with {len(filtered_tools)} tools")
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize MCP tools: {e}")
            raise

    def get_entrypoint_for_tool(self, tool: dict):
        """
        Return an entrypoint for an MCP tool.

        Args:
            tool: The MCP tool to create an entrypoint for.

        Returns:
            Callable: The entrypoint function for the tool.
        """

        async def call_tool(agent: Agent, tool_name: str, **kwargs) -> str:
            try:
                log_debug(f"Calling MCP Tool '{tool_name}' with args: {kwargs}")
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.sse_url}/call-tool/{tool_name}",
                        json=kwargs,
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"Error from MCP tool '{tool_name}': {response.status}")
                        async for line in response.content:
                            if line.startswith(b"data: "):
                                event_data = line[6:].decode("utf-8").strip()
                                log_debug(f"Received SSE data: {event_data}")
                                # Process the event data
                                return self.process_tool_response(agent, event_data)

            except Exception as e:
                logger.exception(f"Failed to call MCP tool '{tool_name}': {e}")
                return f"Error: {e}"

        return partial(call_tool, tool_name=tool["name"])

    def process_tool_response(self, agent: Agent, event_data: str) -> str:
        """
        Process the response from an MCP tool.

        Args:
            agent: The agent using the tool.
            event_data: The data received from the SSE server.

        Returns:
            str: The processed response.
        """
        try:
            # Parse the event data (assuming JSON format)
            import json

            data = json.loads(event_data)
            response_str = ""

            for content_item in data.get("content", []):
                if content_item["type"] == "text":
                    response_str += content_item["text"] + "\n"
                elif content_item["type"] == "image":
                    # Handle image content if present
                    img_artifact = ImageArtifact(
                        id=str(uuid4()),
                        url=content_item.get("url"),
                        base64_data=content_item.get("data"),
                        mime_type=content_item.get("mimeType", "image/png"),
                    )
                    agent.add_image(img_artifact)
                    response_str += "Image has been generated and added to the response.\n"
                elif content_item["type"] == "embedded_resource":
                    # Handle embedded resources
                    response_str += f"[Embedded resource: {content_item['resource']}]\n"
                else:
                    # Handle other content types
                    response_str += f"[Unsupported content type: {content_item['type']}]\n"

            return response_str.strip()
        except Exception as e:
            logger.exception(f"Failed to process tool response: {e}")
            return f"Error processing response: {e}"