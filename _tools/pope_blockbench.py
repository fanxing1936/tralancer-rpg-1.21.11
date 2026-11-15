"""教皇专用本机 Blockbench MCP 客户端；仅操作明确指定的新项目。"""
import json
import urllib.request


class BlockbenchMCP:
    def __init__(self, port=52907):
        self.url=f'http://127.0.0.1:{port}/bb-mcp'
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.session=None
        self.sequence=0
        self.rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'pope-model-authoring','version':'1.0'}})
        self.rpc('notifications/initialized',notification=True)

    def rpc(self,method,params=None,notification=False):
        self.sequence+=1
        body={'jsonrpc':'2.0','method':method}
        if params is not None: body['params']=params
        if not notification: body['id']=self.sequence
        headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'}
        if self.session: headers['Mcp-Session-Id']=self.session
        request=urllib.request.Request(self.url,data=json.dumps(body).encode(),headers=headers)
        with self.opener.open(request,timeout=55) as response:
            self.session=response.headers.get('Mcp-Session-Id',self.session)
            raw=response.read().decode('utf-8')
        if not raw:return {}
        if raw.startswith(('event:','data:')):raw=next(line[6:] for line in raw.splitlines() if line.startswith('data: '))
        payload=json.loads(raw)
        if 'error' in payload:raise RuntimeError(payload['error'])
        return payload.get('result',{})

    def tool(self,name,arguments=None):
        result=self.rpc('tools/call',{'name':name,'arguments':arguments or {}})
        if result.get('isError'):raise RuntimeError(result)
        return result

    def evaluate(self,code):
        result=self.tool('risky_eval',{'code':code})
        text=next(b['text'] for b in result['content'] if b['type']=='text')
        try:value=json.loads(text)
        except ValueError:value=text
        if isinstance(value,str) and value.startswith('Error executing code:'):
            raise RuntimeError(value)
        return value


if __name__=='__main__':
    client=BlockbenchMCP()
    for t in client.rpc('tools/list')['tools']:
        if t['name'] in ('create_project','get_project_info','risky_eval','capture_screenshot','save_project','list_projects'):
            print(json.dumps(t,ensure_ascii=False))
