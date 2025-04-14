from agno.agent import Agent

def demo_echo_mcp():
    # Khởi tạo agent
    agent = Agent()
    
    # Định nghĩa thông tin server và tool
    server_name = "github.com/Garoth/echo-mcp"
    tool_name = "echo"
    
    # Tạo message để gửi
    message = "Xin chào! Đây là ví dụ về Echo MCP Server."
    
    # Chuẩn bị arguments cho tool
    arguments = {
        "message": message
    }
    
    try:
        # Gọi MCP tool
        result = agent.use_mcp_tool(
            server_name=server_name,
            tool_name=tool_name,
            arguments=arguments
        )
        
        # In kết quả
        print("Tin nhắn gốc:", message)
        print("Phản hồi từ Echo Server:", result)
        
    except Exception as e:
        print("Lỗi:", str(e))

if __name__ == "__main__":
    demo_echo_mcp()
