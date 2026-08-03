import os
from typing import Dict, Any, List

class FileSystemMCP:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        path = arguments.get("path", "")
        full_path = os.path.join(self.root_dir, path)
        if tool_name == "list_files":
            return os.listdir(full_path)
        elif tool_name == "read_file":
            with open(full_path, "r") as f:
                return f.read()
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
