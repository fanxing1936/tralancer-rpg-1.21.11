"""Heart of Ender 的本机 Blockbench MCP 客户端；不修改共用生成管线。

连接已安装的 MCP Server 插件。端口在 Blockbench 设置中指定，默认值为本次
会话使用的 52907。所有输出仅写到本任务目录；不读取/覆盖其他已打开的工程。
"""
from __future__ import annotations

import argparse
import base64
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REF = ROOT / "heart_of_ender_ref"


class BlockbenchMCP:
    def __init__(self, port: int = 52907):
        self.url = f"http://localhost:{port}/bb-mcp"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.session = None
        self.sequence = 0
        self.rpc("initialize", {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "heart-of-ender-authoring", "version": "1.0"},
        })
        self.rpc("notifications/initialized", notification=True)

    def rpc(self, method, params=None, notification=False):
        self.sequence += 1
        body = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            body["params"] = params
        if not notification:
            body["id"] = self.sequence
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        with self.opener.open(urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers), timeout=60) as response:
            self.session = response.headers.get("Mcp-Session-Id", self.session)
            raw = response.read().decode("utf-8")
        if not raw:
            return {}
        if raw.startswith("event:") or raw.startswith("data:"):
            raw = next(line[6:] for line in raw.splitlines() if line.startswith("data: "))
        payload = json.loads(raw)
        if "error" in payload:
            raise RuntimeError(payload["error"])
        return payload.get("result", {})

    def tool(self, name, arguments=None):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments or {}})
        if result.get("isError"):
            raise RuntimeError(result)
        return result

    def evaluate(self, code):
        return self.tool("risky_eval", {"code": code})

    def screenshot(self, path):
        result = self.tool("capture_screenshot", {"project": "heart_of_ender"})
        for item in result.get("content", []):
            if item.get("type") == "image":
                Path(path).write_bytes(base64.b64decode(item["data"]))
                return
        raise RuntimeError("Blockbench 没有返回截图")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=52907)
    parser.add_argument("--tool", default="get_project_info")
    parser.add_argument("--arguments", default="{}")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    client = BlockbenchMCP(args.port)
    result = client.tool(args.tool, json.loads(args.arguments))
    if args.output:
        target = args.output.resolve()
        if not target.is_relative_to(REF.resolve()):
            raise ValueError("输出必须位于 heart_of_ender_ref 中")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(target)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
