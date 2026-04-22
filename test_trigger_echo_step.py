import asyncio
from envs.echo_env.client import EchoEnv

async def main():
    async with EchoEnv(base_url="http://localhost:8000") as env:
        await env.reset()
        tools = await env.list_tools()
        print("Available tools:", [t.name for t in tools])
        result = await env.call_tool("echo_message", message="Hello from test!")
        print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
