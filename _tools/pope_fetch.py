#!/usr/bin/env python3
"""教皇 M1：浏览器从公开 Wiki 下载，原样 POST 到仅监听本机的接收器。"""
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

REF = Path(__file__).resolve().parent / 'pope_ref'
PORT = 8878
HTML = r'''<!doctype html><html lang="zh"><meta charset="utf-8">
<title>教皇 M1 素材接收</title>
<style>body{font:16px system-ui;max-width:1000px;margin:30px auto}textarea{width:100%;height:160px}pre{white-space:pre-wrap}button{padding:12px;margin:10px}</style>
<h1>教皇 M1：原始素材下载</h1><p>只下载清单中的公开 Wiki 文件；保留原文件名；不下载 Music 或末影之心音效。</p>
<label for="manifest">经页面核实的素材清单</label><textarea id="manifest"></textarea>
<button id="save">保存清单</button><button id="download">下载缺失素材</button><pre id="log">等待清单</pre>
<script>
const log=document.getElementById('log');
document.getElementById('save').onclick=async()=>{const r=await fetch('/manifest',{method:'POST',body:document.getElementById('manifest').value});log.textContent=await r.text()};
document.getElementById('download').onclick=async()=>{
const m=await(await fetch('/manifest')).json();log.textContent='开始 '+m.assets.length+' 个文件\n';
let ok=0,fail=0;
for(const a of m.assets){try{
const s=await(await fetch('/status?file='+encodeURIComponent(a.path))).json();
if(s.exists){ok++;log.textContent+='已有 '+a.path+'\n';continue}
const r=await fetch(a.url,{credentials:'omit',signal:AbortSignal.timeout(45000)});
if(!r.ok)throw Error('远端 HTTP '+r.status);
const b=await r.arrayBuffer();
const p=await fetch('/receive?file='+encodeURIComponent(a.path),{method:'POST',headers:{'X-Source-URL':r.url,'X-Source-Type':r.headers.get('content-type')||''},body:b});
if(!p.ok)throw Error(await p.text());ok++;log.textContent+='成功 '+a.path+' '+b.byteLength+' bytes\n';
}catch(e){fail++;log.textContent+='失败 '+a.path+' '+e.message+'\n'}}
log.textContent+='下载结束：成功 '+ok+'，失败 '+fail+'。请进行本地校验。'};
</script></html>'''

def save_new(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        if p.read_bytes() != data:
            raise ValueError('已有文件内容不同，不覆盖：' + str(p))
    else:
        p.write_bytes(data)

def target(name):
    p = (REF / name).resolve()
    if not p.is_relative_to(REF.resolve()) or p == REF.resolve():
        raise ValueError('路径超出 pope_ref')
    return p

class Handler(BaseHTTPRequestHandler):
    def reply(self, obj, status=200, mime='application/json; charset=utf-8'):
        data=(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False)).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        q=urlparse(self.path)
        if q.path=='/': self.reply(HTML,mime='text/html; charset=utf-8')
        elif q.path=='/manifest': self.reply((REF/'source_manifest.json').read_text(encoding='utf-8'))
        elif q.path=='/status': self.reply({'exists':target(parse_qs(q.query)['file'][0]).is_file()})
        else: self.reply('不存在',404)

    def do_POST(self):
        try:
            q=urlparse(self.path)
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<128*1024*1024: raise ValueError('大小超限')
            data=self.rfile.read(size)
            if q.path=='/manifest':
                m=json.loads(data)
                for a in m['assets']:
                    target(a['path'])
                    u=urlparse(a['url'])
                    if u.scheme!='https' or u.netloc!='minecraft.wiki' or not u.path.startswith('/images/'): raise ValueError('非公开 Wiki 素材')
                    name=Path(unquote(u.path)).name
                    if any(s in name.lower() for s in ('bgm_', 'archvessel', 'archvisage')): raise ValueError('排除音乐和末影之心音效')
                    if Path(a['path']).name != name: raise ValueError('必须保留原文件名')
                save_new(REF/'source_manifest.json',(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
                self.reply('已保存清单：'+str(len(m['assets']))+' 个文件')
            elif q.path=='/receive':
                name=parse_qs(q.query)['file'][0]
                m=json.loads((REF/'source_manifest.json').read_text(encoding='utf-8'))
                if name not in {a['path'] for a in m['assets']}: raise ValueError('不在清单')
                p=target(name)
                magic={'.png':b'\x89PNG\r\n\x1a\n','.gif':b'GIF8','.ogg':b'OggS','.jpg':b'\xff\xd8'}
                if p.suffix not in magic or not data.startswith(magic[p.suffix]): raise ValueError('格式签名错误')
                save_new(p,data)
                with (REF/'download_log.jsonl').open('a',encoding='utf-8',newline='\n') as f:
                    f.write(json.dumps({'path':name,'bytes':size,'sha256':hashlib.sha256(data).hexdigest(),'response_url':self.headers.get('X-Source-URL'),'content_type':self.headers.get('X-Source-Type')},ensure_ascii=False)+'\n')
                self.reply({'saved':name,'bytes':size})
            else: self.reply('不存在',404)
        except Exception as exc: self.reply(str(exc),400)

if __name__=='__main__':
    print(f'打开 http://127.0.0.1:{PORT}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
