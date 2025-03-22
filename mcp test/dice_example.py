from agno.agent import Agent

def demo_dice_roll():
    # Khởi tạo agent
    agent = Agent()
    
    # Định nghĩa thông tin server và tool
    server_name = "dice-server"
    tool_name = "roll_dice"
    
    # Chuẩn bị arguments cho tool
    arguments = {
        "sides": 6,  # Số mặt của xúc xắc
        "count": 2   # Số lượng xúc xắc cần tung
    }
    
    try:
        # Gọi MCP tool
        result = agent.use_mcp_tool(
            server_name=server_name,
            tool_name=tool_name,
            arguments=arguments
        )
        
        # In kết quả
        print("Kết quả tung xúc xắc:")
        print(result)
        
    except Exception as e:
        print("Lỗi:", str(e))

if __name__ == "__main__":
    demo_dice_roll()
