# 路西法动作来源、技能时序与重定向依据

当前只完成原动作读取与静态数学验证；最终动作、Blockbench逐帧外观和真实游戏时序尚未在本子任务验收。没有修改技能代码或模型。

完整源文件：`necromancer_animation_source.json`，SHA256 `930867a3022a9544915e48f83c192d18be970d29777e731b6b4bec9f478bfcd1`，已冻结。
7 段原始 PSA 共 19,721 个骨关键帧；35 根原 mesh 骨与 37 条 PSA track 均保存，另含 Mossy 22 骨的映射、局部/世界 bind 矩阵。

## 8 段交付动作的来源

|顺序|clip|来源|原始有效时长/s|接入要求|
|---:|---|---|---:|---|
|0|idle|original Necromancer Idle PSA|6.208334|原动作重定向到 Mossy 22 骨；持矛姿态另记录。|
|1|walk|original Necromancer Walk PSA upper body; project Sunken walk leg phase reference|0.791667|原上身曲线保留；下身悬浮改成双腿交替行走，这是用户要求的适配。Sunken 腿关键点 R(+25,-25,+25)、L(-25,+25,-25) 度，t=0,.5,1s，只提供步态幅度/相位参考，不能直接加到新骨架欧拉角。|
|2|attack|original Necromancer BasicAttack PSA|1.458333|法杖动作改为握蛇矛向前刺；选定释放/有效帧裁为 t=0，再恢复。不得把未核实的源帧当原游戏伤害事件。|
|3|strong|original Necromancer StrongAttack PSA|1.916667|对立即生效的重招将释放/重击姿态放在 t=0；后续恢复保留源动作依据。|
|4|cast|project leviathan animation.cast|1.200000|legacy cast 总长1.2s、原释放 cue 0.65s；不能原封不动接立即生效技能。将释放姿态裁首或调整时间为0，保留完整原时间映射。|
|5|laugh|original Necromancer Novelty PSA|3.291667|用于30tick/1.5s大招警告。可裁选/重定时覆盖1.5s，或被 strong 在第30tick明确接管；原3.2916667s整段不能被称已完整播完。|
|6|stun|original Necromancer Stun PSA|1.625000|绑定驱魔束缚状态；结束/持有策略由运行时明确处理。未在本任务读取完整束缚运行时，不能声明已验证触发。|
|7|rise|project leviathan animation.rise|2.400000|沿用项目登场轨迹并重定向；原 SkeletonNecromancer/Animations 索引没有名为 Rise 或 Summon 的序列。Sleeping 不自动等同 Rise。|

上表时长是来源，不是已经制作完成的最终 clip 时长。GetHitFront 原数据另保存用于参考，不新增交付 clip。

StrongAttack 的原 SequenceLength=2.875s、RateScale=1.5，所以实际 PSA 播放时长为1.91666668s。PSA Time=1 是一帧单位；秒数必须用 frame/AnimRate。UModel props 的事件名称没有足够可靠的触发时间，不能据此编造原出手帧。

## 技能生效时刻

|钩子|建议clip|直接效果/伤害|对齐|
|---|---|---|---|
|sk1_1|attack|沿视线召唤8个尖牙；起手/蛇矛释放在0tick。|本hook0tick|
|sk1_2|attack|^1..9九个位置命令同步执行，不是9tick序列；同次函数里伤害/缓速。|本hook0tick|
|sk1_3|cast|漂浮与魔法伤害立即下发。|本hook0tick|
|sk1_4|strong|漂浮/虚弱与魔法伤害立即下发；后续跌落不是本函数延迟伤害命令。|本hook0tick|
|sk1_5|strong|立即击退式传送、魔法伤害、缓速。|本hook0tick|
|ult1_warn|laugh|只发提示、粒子、音效；30tick后由 ult1 接管。|本hook0tick|
|ult1|strong|立即18伤害和漂浮；尖牙另按自己的实体计时延迟伤害。|警告后30tick，即本hook0tick|

沿视线的 sk1_1、sk1_2 均用 attack。sk1_2 的9个采样位置同一tick执行，不能按1到9tick分段。普通招式没有现成蓄力延迟，动作需以释放/命中姿态开始，再恢复；不能为了保留动作前摇而改战斗函数。

大招：ult_start 写入30并立即警告；每次 ult_tick 先 charge 再减1，因此额外 charge 脉冲在第11/21次更新，结算在第30次更新，即20TPS下1.5s。若束缚状态暂停推进，真实墙钟时间随运行时暂停；这里记录的是更新序号。

尖牙：Java1.21.11映射与本机字节码证明伤害判断是 `--warmupDelayTicks == -8`。原罪 Warmup2,4,…16 对应第10,12,…24次尖牙实体更新；大招 Warmup4/8/12对应第12/16/20次更新。大招另有警告后第30tick的立即18伤害。实体生成的世界tick相位未在游戏实测，因此不要把更新序号伪装为录制测量。

## 22 骨重定向

所有公共 J_* 关节的 bind 框架几乎重合；名称确实是 J_L_Hip / J_L_Spine，不要虚构 J_Hip / J_Spine 别名。body/head/R_arm/R_leg/L_leg 几何marker的原点或朝向与Mossy不同；6个marker的局部位置在7段原动作中均恒定。

旋转先算源世界旋转变化，再施加于目标bind：

```text
Rt_world(t) = Rs_world(t) · inverse(Rs_bind_world) · Rt_bind_world
Rt_local(t) = inverse(Rt_parent_world(t)) · Rt_world(t)
pt_local(t) = pt_bind_local + inverse(Rt_parent_bind_world) · Rs_parent_bind_world · (ps_local(t) - ps_bind_local)
```

根骨父变换取单位矩阵。位移保留目标骨长/marker偏移，再传源局部位移变化；不能冻结所有J_*位置，手部真实动作位移明显。也不要对不同marker直接套完整SE(3) world delta，它会用源/目标原点差产生额外杠杆位移；本次7段中实测差异最大约0.00897239px。

源参考用PSA保存的USkeleton refpose，目标用body输入bind。完整JSON同时保存glTF mesh bind与两者差值。PSA参考与动画key经历的UModel镜像/根骨共轭流程不同，不能共用转换式。BONENAMES父索引是导出器占位；真实父级来自配套glTF。末两条 Staff1/crown1 不属于35骨mesh，不新增幽灵骨。

最终只在序列化时转目标local quaternion为Blockbench实际Euler顺序、解包连续角度，再减目标native rest Euler。不能用源Euler直接叠到目标rest。动画第0帧是源站姿，不等于bind；进入动画的混合须单独记录。

## 独立验证和边界

`necromancer_animation_source_audit.json`：原19721键float32字节逐字节吻合；Java位置矩阵误差0.0；旋转矩阵最大误差6.66e-16；零动作回目标bind的世界矩阵误差5.33e-14。

`audit_animation_source.py` 的 `reference_frame()` 可只读提供任意原动作时间点的目标局部/世界矩阵，供后续native payload对比。适配过的腿部、持矛和出手裁首需带来源时间/骨排除表，不能拿其偏差冒充源转换错误。

未操作Blockbench，未更改模型、游戏安装、战斗逻辑、其他怪或构建脚本。本证据不能替代动作并排图、游戏内换装/技能检查、清理测试或检查点B验收。

## 原始实现依据

- [UEViewer PSA结构](https://github.com/gildor2/UEViewer/blob/master/Exporters/Psk.h)
- [UEViewer PSA导出镜像、帧与占位父级](https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportPsk.cpp)
- [UEViewer glTF坐标转换及根骨共轭](https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportGLTF.cpp)
- [UEViewer UE4动画解压、FixRotationKeys、播放率](https://github.com/gildor2/UEViewer/blob/master/Unreal/UnrealMesh/UnAnim4.cpp)
- [Mojang 1.21.11官方client mappings](https://piston-data.mojang.com/v1/objects/031a68bebf55d824f66d6573d8c752f0e1bf232a/client.txt)

具体本机路径、文件SHA、源码下载副本、字节码读证及每条技能函数快照hash见 `animation_timing.json`。
