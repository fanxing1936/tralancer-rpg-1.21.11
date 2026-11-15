#!/usr/bin/env python3
"""Archive public Minecraft Wiki media via a local browser receiver.

Run this script, open http://127.0.0.1:8876, paste the observed-page
manifest, then click Save manifest and Download. No credentials are used.
Only the two task reference directories are writable; existing identical
files are retained and differing files are never overwritten.
"""
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HERE = Path(__file__).resolve().parent
REF = HERE / "heart_of_ender_ref"
PAGE = "https://minecraft.wiki/w/Dungeons:Heart_of_Ender"
ALLOWED = {"heart_of_ender_ref", "arch_visage_ref"}
HTML = r'''<!doctype html><html lang="zh"><meta charset="utf-8">
<title>末影之心 M1 素材接收</title>
<style>body{font:16px system-ui;max-width:1100px;margin:30px auto;background:#131821;color:#e3e7ef}textarea{width:100%;height:150px}button{padding:12px;margin:10px 10px 10px 0}pre{white-space:pre-wrap}</style>
<h1>末影之心 M1 素材接收</h1><p>从公开 Wiki 媒体地址获取，原样保存到本机任务目录；不下载 Music。</p>
<label for="manifest">已观测的素材清单 JSON</label><textarea id="manifest"></textarea>
<button id="save">保存清单</button><button id="download">下载缺失素材</button><pre id="log">等待清单</pre>
<script>
const log=document.getElementById('log');
document.getElementById('save').onclick=async()=>{
 const r=await fetch('/manifest',{method:'POST',headers:{'Content-Type':'application/json'},body:document.getElementById('manifest').value});
 log.textContent=await r.text();
};
document.getElementById('download').onclick=async()=>{
 const m=await (await fetch('/manifest')).json(); log.textContent='开始 '+m.assets.length+' 个文件\n';
 for(const a of m.assets){
  try{
   const s=await (await fetch('/status?file='+encodeURIComponent(a.path))).json();
   if(s.exists){log.textContent+='已有 '+a.path+'\n';continue;}
   const r=await fetch(a.url,{credentials:'omit',signal:AbortSignal.timeout(90000)});
   if(!r.ok)throw new Error('远端 HTTP '+r.status);
   const b=await r.arrayBuffer();
   const p=await fetch('/receive?file='+encodeURIComponent(a.path),{method:'POST',headers:{'X-Source-URL':r.url,'X-Source-Type':r.headers.get('content-type')||''},body:b});
   if(!p.ok)throw new Error(await p.text());
   log.textContent+='成功 '+a.path+' '+b.byteLength+' bytes\n';
  }catch(e){log.textContent+='失败 '+a.path+' '+e.message+'\n';}
 }
 log.textContent+='下载结束；请运行本地校验。';
};
</script></html>'''


def save_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError("Refusing to overwrite different existing file: " + str(path))
    else:
        path.write_bytes(data)


def target(value):
    p = Path(value)
    if p.is_absolute() or len(p.parts) < 2 or p.parts[0] not in ALLOWED or ".." in p.parts:
        raise ValueError("Invalid task path")
    resolved = (HERE / p).resolve()
    # Resolve junctions/symlinks before accepting a write, even on later runs.
    expected_root = HERE / p.parts[0]
    if not resolved.is_relative_to(expected_root):
        raise ValueError("Resolved path escapes task reference directory")
    return resolved


class Handler(BaseHTTPRequestHandler):
    def reply(self, value, status=200, mime="application/json; charset=utf-8"):
        data = value.encode("utf-8") if isinstance(value, str) else json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        req = urlparse(self.path)
        if req.path == "/":
            self.reply(HTML, mime="text/html; charset=utf-8")
        elif req.path == "/manifest":
            self.reply((REF / "source_manifest.json").read_text(encoding="utf-8"))
        elif req.path == "/status":
            p = target(parse_qs(req.query)["file"][0])
            self.reply({"exists": p.is_file()})
        else:
            self.reply("Not found", 404)

    def do_POST(self):
        try:
            req = urlparse(self.path)
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size <= 256 * 1024 * 1024:
                raise ValueError("Invalid body size")
            data = self.rfile.read(size)
            if req.path == "/manifest":
                manifest = json.loads(data)
                for a in manifest["assets"]:
                    target(a["path"])
                    u = urlparse(a["url"])
                    if u.scheme != "https" or u.netloc != "minecraft.wiki" or not u.path.startswith("/images/"):
                        raise ValueError("Only observed public Minecraft Wiki media are accepted")
                    if Path(unquote(u.path)).name.lower().startswith("bgm_"):
                        raise ValueError("Music excluded")
                save_new(REF / "source_manifest.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
                self.reply("已保存清单：%d 个文件" % len(manifest["assets"]))
            elif req.path == "/receive":
                name = parse_qs(req.query)["file"][0]
                manifest = json.loads((REF / "source_manifest.json").read_text(encoding="utf-8"))
                if name not in {a["path"] for a in manifest["assets"]}:
                    raise ValueError("File not in observed manifest")
                p = target(name)
                ext = p.suffix.lower()
                magic = {".png": b"\x89PNG\r\n\x1a\n", ".gif": b"GIF8", ".ogg": b"OggS", ".jpg": b"\xff\xd8"}
                if ext in magic and not data.startswith(magic[ext]):
                    raise ValueError("Wrong media signature (possibly an HTML challenge)")
                if ext == ".mp4" and data[4:8] != b"ftyp":
                    raise ValueError("Wrong MP4 signature")
                save_new(p, data)
                with (REF / "download_log.jsonl").open("a", encoding="utf-8", newline="\n") as f:
                    f.write(json.dumps({"path":name,"bytes":size,"sha256":hashlib.sha256(data).hexdigest(),"response_url":self.headers.get("X-Source-URL"),"content_type":self.headers.get("X-Source-Type")}, ensure_ascii=False)+"\n")
                self.reply({"saved":name,"bytes":size})
            else:
                self.reply("Not found", 404)
        except Exception as exc:
            self.reply(str(exc), 400)


if __name__ == "__main__":
    print("Open http://127.0.0.1:8876 in the browser", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8876), Handler).serve_forever()
