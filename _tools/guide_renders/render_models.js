// 图鉴第 VIII 节的模型渲染图（2026-11-15）。在 Blockbench 5.2 里运行（Blockbench MCP 的 risky_eval，或开发者控制台）。
// 每个模型：打开 .bbmodel → 摆到待机动作第 0 刻 → 按包围盒正交取景（左前上方 35°/12°）→ 透明背景 900×900 PNG。
// 原作转换出来的方块常只写了部分面，Blockbench 5.2 读取会报错，所以载入前把缺的面补成空面。
// 出图后在 _tools 下运行：python guide_renders/make_web.py（裁边、缩到 360、存 webp）。
// 只关闭自己打开的工程；你原来开着的工程不动。
//
// 特例：猪灵商人、坩埚、猪灵原作朝 +z，从背面取景；塔卫的大盾会挡住身体，改从右前方；
// 雅克隐藏四个阶段的竖琴弩（常态只拿刀）；首席附魔师换成资源包里重着色后的白金贴图（王冠没有画进去）。

const ROOT = 'D:/agent/claude/github-create/tralancer-rpg-1.21.11/';
const T = ROOT + '_tools/';
const OUT = T + 'guide_renders/';
const fs = require('fs'), path = require('path');
const wait = ms => new Promise(r => setTimeout(r, ms));

function load(p) {
  const m = JSON.parse(fs.readFileSync(p, 'utf8'));
  const F = ['north', 'east', 'south', 'west', 'up', 'down'];
  (m.elements || []).forEach(e => {
    if ((e.type || 'cube') === 'cube') { e.faces = e.faces || {}; F.forEach(f => { if (!e.faces[f]) e.faces[f] = {uv: [0, 0, 0, 0], texture: null}; }); }
  });
  setupProject(Formats[m.meta && m.meta.model_format] || Formats.free);
  Codecs.project.load(m, {path: p, name: path.basename(p)});
}

function pose(pref) {
  const anims = Animation.all || [];
  if (!anims.length) return 'none';
  let a = null;
  for (const k of pref) { a = anims.find(x => x.name.toLowerCase() === k) || anims.find(x => x.name.toLowerCase().includes(k)); if (a) break; }
  (a || anims[0]).select(); Timeline.setTime(0); Animator.preview();
  return (a || anims[0]).name;
}

function render(out, opt) {
  const W = 900, r = new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: true});
  r.setSize(W, W); r.setClearColor(0x000000, 0);
  const hidden = [];
  scene.children.forEach(o => { if (o !== Project.model_3d && !o.isLight && o.visible) { hidden.push(o); o.visible = false; } });
  Project.model_3d.traverse(o => { if (o.visible && (o.isLineSegments || o.isLine)) { hidden.push(o); o.visible = false; } });
  Project.model_3d.updateMatrixWorld(true);
  const box = new THREE.Box3();
  Project.model_3d.traverse(o => { if (o.isMesh && o.visible) { o.geometry.computeBoundingBox(); const b = o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld); if (isFinite(b.min.x)) box.union(b); } });
  const c = box.getCenter(new THREE.Vector3());
  const yaw = (opt.yaw == null ? -35 : opt.yaw) * Math.PI / 180, pitch = 12 * Math.PI / 180;
  const dir = new THREE.Vector3(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch));
  if (opt.back) { dir.x *= -1; dir.z *= -1; }
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 100000);
  cam.position.copy(c).addScaledVector(dir, 5000); cam.lookAt(c); cam.updateMatrixWorld(true);
  let m = 0;
  for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
    const v = new THREE.Vector3(x, y, z).applyMatrix4(cam.matrixWorldInverse); m = Math.max(m, Math.abs(v.x), Math.abs(v.y));
  }
  const rad = m * 1.04; cam.left = -rad; cam.right = rad; cam.top = rad; cam.bottom = -rad; cam.updateProjectionMatrix();
  r.render(scene, cam);
  fs.writeFileSync(out, Buffer.from(r.domElement.toDataURL('image/png').split(',')[1], 'base64'));
  hidden.forEach(o => o.visible = true); r.dispose(); r.forceContextLoss();
}

async function job(key, rel, opt = {}) {
  const before = new Set(ModelProject.all.map(x => x.uuid));
  try {
    load(T + rel); await wait(1200);
    const t = ModelProject.all.filter(x => !before.has(x.uuid)).find(x => x.elements && x.elements.length);
    if (t && t !== Project) { t.select(); await wait(400); }
    if (opt.texture) { Texture.all[0].fromPath(ROOT + opt.texture); await wait(1500); }
    pose(['animation.idle', 'idle']); await wait(300);
    if (opt.hide) { Group.all.filter(g => opt.hide.test(g.name)).forEach(g => { g.visibility = false; g.forEachChild(c => { c.visibility = false; }, OutlinerElement); }); Canvas.updateVisibility(); }
    render(OUT + key + '.png', opt);
  } finally {
    for (const x of ModelProject.all.filter(x => !before.has(x.uuid))) { try { await x.close(true); } catch (_) {} }
  }
}

const JOBS = [
  ['lucifer', 'lucifer_ref/lucifer.bbmodel'],
  ['leviathan', 'leviathan_dungeons_ref/leviathan.bbmodel'],
  ['abaddon', 'abaddon_dungeons_ref/abaddon.bbmodel'],
  ['beelzebub', 'beelzebub_dungeons_ref/beelzebub.bbmodel'],
  ['samael_lord', 'samael_lord_dungeons_ref/samael_lord.bbmodel'],
  ['belial_lord', 'belial_lord_dungeons_ref/belial_lord.bbmodel', {back: true}],
  ['mammon_lord', 'mammon_lord_dungeons_ref/mammon_lord.bbmodel', {back: true}],
  ['lucifer_servant', 'lucifer_servant_dungeons_ref/lucifer_servant.bbmodel'],
  ['sunken_skeleton', 'sunken_skeleton_dungeons_ref/sunken_skeleton.bbmodel'],
  ['tower_wraith', 'tower_wraith_dungeons_ref/tower_wraith.bbmodel'],
  ['vanguard', 'vanguard_dungeons_ref/vanguard.bbmodel'],
  ['samael_servant', 'samael_servant_dungeons_ref/samael_servant.bbmodel'],
  ['belial_servant', 'belial_servant_dungeons_ref/belial_servant.bbmodel'],
  ['mammon_servant', 'mammon_servant_dungeons_ref/mammon_servant.bbmodel', {back: true}],
  ['tower_guard', 'tower_guard_dungeons_ref/tower_guard.bbmodel', {yaw: 55}],
  ['royal_guard', 'royal_guard_dungeons_ref/royal_guard.bbmodel'],
  ['end_illager', 'end_illager_dungeons_ref/end_illager.bbmodel'],
  ['pope', 'pope_dungeons_ref/pope.bbmodel'],
  ['heart_of_ender', 'heart_of_ender_ref/heart_of_ender.bbmodel'],
  ['arch_visage', 'arch_visage_ref/arch_visage.bbmodel'],
  ['lucifer_p2', 'lucifer_p2_ref/lucifer_p2.bbmodel'],
  ['usurper', 'usurper_dungeons_ref/usurper.bbmodel'],
  ['prime_enchanter', 'prime_enchanter_ref/prime_enchanter.bbmodel', {texture: 'resourcepack/assets/rpg/textures/item/prime_enchanter/atlas.png'}],
  ['jacques', 'jacques_dungeons_ref/jacques.bbmodel', {hide: /^harp\d/}],
  ['david', 'david_dungeons_ref/david.bbmodel'],
];

// 一次跑几个即可（MCP 单次调用有超时；lucifer_p2 有 16 MB，单独跑）。
(async () => { for (const [k, p, o] of JOBS) await job(k, p, o); })();
