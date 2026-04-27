# MCP Environment Implementation Guide

This guide explains how to implement and debug MCP (Model Context Protocol) environments in OpenEnv, with a focus on the lifecycle and invocation of the `step` method.

## Overview
MCP environments in OpenEnv allow for tool-based, agentic interaction patterns. The core lifecycle methods are typically `reset` and `step`, which are called by the client to interact with the environment.

## Common Pitfall: `step` Not Invoked
A frequent source of confusion is when the `step` method is not called as expected. This usually happens due to one of the following:
- The environment is not registered correctly with the MCP server.
- The client is not sending the correct tool/action invocation.
- The server-side handler for the tool/action is missing or misnamed.

## Example: Working MCP Environment
See [PR #446](https://github.com/meta-pytorch/OpenEnv/pull/446) for a complete, working MCP environment implementation. This PR demonstrates:
- Proper registration of tools/actions
- Correct implementation of the `step` method
- End-to-end invocation from client to environment

## Debugging Tips
- Add print/log statements to both `reset` and `step` methods to confirm invocation.
- Ensure your tool/action names match between client and server.
- Check that your Docker image or local server is running the latest code.
- Use the `list_tools()` method on the client to verify available actions.

## Minimal Example
```python
# server/your_environment.py
class YourEnv(MCPEnvironment):
    def reset(self, ...):
        print("reset called")
        ...
    def step(self, action):
        print("step called with", action)
        ...
```

```python
# client
async with YourEnv.from_docker_image("your_env:latest") as env:
    await env.reset()
    await env.step(YourAction(...))
```

## References
- [PR #446: Working MCP Environment Example](https://github.com/meta-pytorch/OpenEnv/pull/446)
- [envs/finqa_env/server/finqa_environment.py](https://github.com/meta-pytorch/OpenEnv/blob/main/envs/finqa_env/server/finqa_environment.py)
- [envs/echo_env/server/echo_environment.py](https://github.com/meta-pytorch/OpenEnv/blob/main/envs/echo_env/server/echo_environment.py)

---
If you encounter issues, check the above points and refer to the linked PR for a working pattern.
