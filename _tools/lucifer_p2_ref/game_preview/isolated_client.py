"""Launch the existing vanilla client with a wholly separate writable gameDir."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, sys, uuid, zipfile

HERE = Path(__file__).resolve().parent
REPO = Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11')
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPO / '_tools'))
import mc_env

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def allowed(lib):
    if lib['name'].startswith(('net.fabricmc:', 'net.fabricmc.fabric-api:')):
        return False
    name = lib['name']
    if any(s in name for s in ('natives-windows-arm64', 'natives-windows-x86')):
        return False
    rules = lib.get('rules')
    if not rules:
        return True
    result = False
    for rule in rules:
        spec = rule.get('os', {})
        match = spec.get('name', 'windows') == 'windows'
        match &= spec.get('arch', 'x86_64') in ('x86_64', 'amd64')
        if spec.get('version'):
            match &= bool(re.search(spec['version'], '10.0'))
        if match:
            result = rule['action'] == 'allow'
    return result

def prepare():
    doc = json.loads(Path(mc_env.VJSON).read_text(encoding='utf-8'))
    jar = Path(mc_env.JAR).resolve()
    with zipfile.ZipFile(jar) as z:
        version = json.loads(z.read('version.json'))
        assert version['id'] == '1.21.11', version
    libraries = []
    missing = []
    for lib in doc['libraries']:
        if not allowed(lib):
            continue
        artifact = lib.get('downloads', {}).get('artifact', {})
        rel = artifact.get('path')
        if not rel:
            p = lib['name'].split(':')
            rel = '/'.join((p[0].replace('.', '/'), p[1], p[2], p[1]+'-'+p[2]+('-'+p[3] if len(p)>3 else '')+'.jar'))
        path = (Path(mc_env.LIBS)/rel).resolve()
        if not path.is_file():
            missing.append(str(path))
        else:
            libraries.append(path)
    assert not missing, missing
    game = HERE / 'game'
    natives = HERE / 'natives'
    temporary = HERE / 'tmp'
    for path in (game, natives, temporary, temporary/'lwjgl', temporary/'jna', game/'resourcepacks', HERE/'evidence'):
        path.mkdir(parents=True, exist_ok=True)
    for lib in libraries:
        if 'natives-windows' not in lib.name:
            continue
        with zipfile.ZipFile(lib) as z:
            for n in z.namelist():
                if n.lower().endswith('.dll'):
                    target = natives / Path(n).name
                    data = z.read(n)
                    if target.exists():
                        assert target.read_bytes() == data, ('conflicting native', target)
                    else:
                        target.write_bytes(data)
    index = Path(mc_env.GAME) / 'assets' / 'indexes' / (doc['assetIndex']['id']+'.json')
    assert index.is_file()
    assert hashlib.sha1(index.read_bytes()).hexdigest() == doc['assetIndex']['sha1']
    assets = json.loads(index.read_text(encoding='utf-8'))['objects']
    missing_assets = [name for name, info in assets.items() if not (Path(mc_env.GAME)/'assets'/'objects'/info['hash'][:2]/info['hash']).is_file()]
    assert not missing_assets, missing_assets[:30]
    java = Path(mc_env.JAVA).with_name('javaw.exe')
    assert java.is_file()
    offline = bytearray(hashlib.md5(b'OfflinePlayer:LuciferP2Test').digest())
    offline[6] = (offline[6]&15)|48
    offline[8] = (offline[8]&63)|128
    player_uuid = str(uuid.UUID(bytes=bytes(offline)))
    cmd = [str(java), '-Xms512M', '-Xmx3G', '-Dfile.encoding=UTF-8',
           '-Djava.library.path='+str(natives), '-Djava.io.tmpdir='+str(temporary),
           '-Dorg.lwjgl.system.SharedLibraryExtractPath='+str(temporary/'lwjgl'),
           '-Djna.tmpdir='+str(temporary/'jna'),
           '-cp', os.pathsep.join(map(str, libraries+[jar])), 'net.minecraft.client.main.Main',
           '--username', 'LuciferP2Test', '--version', '1.21.11-isolated-p2',
           '--gameDir', str(game), '--assetsDir', str(Path(mc_env.GAME)/'assets'),
           '--assetIndex', doc['assetIndex']['id'], '--uuid', player_uuid,
           '--accessToken', '0', '--userType', 'legacy', '--versionType', 'release',
           '--width', '1280', '--height', '800']
    record = {'game_dir':str(game), 'username':'LuciferP2Test', 'offline_uuid':player_uuid,
              'main_class':'net.minecraft.client.main.Main', 'fabric_loaded':False,
              'java':str(java), 'jar':str(jar), 'jar_sha256':sha(jar),
              'asset_index':str(index), 'asset_index_sha256':sha(index),
              'asset_objects':len(assets), 'missing_asset_objects':len(missing_assets),
              'library_count':len(libraries), 'libraries':[str(x) for x in libraries],
              'native_dlls':{x.name:sha(x) for x in natives.glob('*.dll')}, 'command':cmd}
    (HERE/'launch_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record

def install_pack(source):
    source = Path(source).resolve()
    destination = HERE/'game'/'resourcepacks'/'LuciferP2-Isolated'
    assert source.is_dir() and (source/'assets').is_dir(), source
    destination.mkdir(parents=True,exist_ok=True)
    shutil.copytree(source,destination,dirs_exist_ok=True)
    if not (destination/'pack.mcmeta').is_file():
        shutil.copy2(REPO/'resourcepack'/'pack.mcmeta',destination/'pack.mcmeta')
    options = HERE/'game'/'options.txt'
    lines = options.read_text(encoding='utf-8').splitlines() if options.exists() else []
    lines = [x for x in lines if not x.startswith(('resourcePacks:', 'incompatibleResourcePacks:'))]
    lines += ['resourcePacks:["vanilla","file/LuciferP2-Isolated"]','incompatibleResourcePacks:[]']
    options.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (HERE/'evidence'/'pack_manifest.json').write_text(json.dumps({str(p.relative_to(destination)):sha(p) for p in destination.rglob('*') if p.is_file()},indent=2),encoding='utf-8')

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['prepare','launch'])
    ap.add_argument('--pack')
    args=ap.parse_args()
    record=prepare()
    if args.pack:
        install_pack(args.pack)
    if args.action=='launch':
        options=HERE/'game'/'options.txt'
        if not options.exists():
            options.write_text('guiScale:2\nmaxFps:60\nrenderDistance:8\nsimulationDistance:5\nfullscreen:false\n',encoding='utf-8')
        log=open(HERE/'client_console.log','ab',buffering=0)
        proc=subprocess.Popen(record['command'],cwd=HERE/'game',stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,
                              creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        (HERE/'client_process.json').write_text(json.dumps({'pid':proc.pid,'game_dir':record['game_dir']},indent=2),encoding='utf-8')
        print('client PID',proc.pid)
    else:
        print(json.dumps({k:v for k,v in record.items() if k not in ('command','libraries','native_dlls')},ensure_ascii=False,indent=2))
