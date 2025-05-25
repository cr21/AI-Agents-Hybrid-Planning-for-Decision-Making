# agent.py

import asyncio
import yaml
from core.loop import AgentLoop
from core.session import MultiMCP
from core.context import MemoryItem, AgentContext
import datetime
from pathlib import Path
import json
import re

def log(stage: str, msg: str):
    """Simple timestamped console logger."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}")

async def main():
    print("🧠 Cortex-R Agent Ready")
    current_session = None

    with open("config/profiles.yaml", "r") as f:
        profile = yaml.safe_load(f)
        mcp_servers_list = profile.get("mcp_servers", [])
        mcp_servers = {server["id"]: server for server in mcp_servers_list}

    multi_mcp = MultiMCP(server_configs=list(mcp_servers.values()))
    await multi_mcp.initialize()

    try:
        while True:
            user_input = input("🧑 What do you want to solve today? → ")
            if user_input.lower() == 'exit':
                break
            if user_input.lower() == 'new':
                current_session = None
                continue

            while True:
                context = AgentContext(
                    user_input=user_input,
                    session_id=current_session,
                    dispatcher=multi_mcp,
                    mcp_server_descriptions=mcp_servers,
                )
                agent = AgentLoop(context)
                if not current_session:
                    current_session = context.session_id

                result = await agent.run()

                if isinstance(result, dict):
                    answer = result["result"]
                    if "FINAL_ANSWER:" in answer:
                        print(f"\n💡 Final Answer: {answer.split('FINAL_ANSWER:')[1].strip()}")
                        break
                    elif "FURTHER_PROCESSING_REQUIRED:" in answer:
                        user_input = answer.split("FURTHER_PROCESSING_REQUIRED:")[1].strip()
                        print(f"\n🔁 Further Processing Required: {user_input}")
                        continue  # 🧠 Re-run agent with updated input
                    else:
                        print(f"\n💡 Final Answer (raw): {answer}")
                        break
                else:
                    print(f"\n💡 Final Answer (unexpected): {result}")
                    break
    except KeyboardInterrupt:
        print("\n👋 Received exit signal. Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())



# Find the ASCII values of characters in INDIA and then return sum of exponentials of those values. -> run successfully
# How much Anmol singh paid for his DLF apartment via Capbridge? -> run successfully
# What do you know about Don Tapscott and Anthony Williams?  -> run successfully
# What is the relationship between Gensol and Go-Auto? -> run successfully
# which course are we teaching on Canvas LMS? "/Users/chiragtagadiya/Downloads/MyProjects/EAG1/AI-Agents-Hybrid-Planning-for-Decision-Making/documents/How to use Canvas LMS.pdf" -> run successfully
# Summarize this page: https://theschoolof.ai/ -> run successfully
# What is the log value of the amount that Anmol singh paid for his DLF apartment via Capbridge?  -> run successfully
