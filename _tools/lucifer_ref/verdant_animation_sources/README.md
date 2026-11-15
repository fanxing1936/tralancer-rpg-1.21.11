> 历史封存说明：本包原 76 个文件对应旧候选 SHA-256 `14931c0cb1584e5da36ff107e0b5bd953d013b0d3f2f385d57a729e36628f197`，下文“最终”及原索引均保留其历史语义，并非当前 final。当前原生导入、保存及重开验证见[verified_clearance](../validation/verified_clearance/README.md)。除本 README 与其 manifest 哈希/字节记录外，原始来源、适配数据和历史索引均保持封存。

# Verdant 路西法：动作与握矛证据包

本包对应最终原生模型 `../separate/lucifer_verdant.bbmodel`，SHA-256 `14931c0cb1584e5da36ff107e0b5bd953d013b0d3f2f385d57a729e36628f197`。不复制最终模型本体；这里只封存其来源、适配输入、脚本和核验结果。原材质 shader 证据已在 `../verdant_sources/material_port/`，不重复封装。

## 原始来源与适配分开记录

| 目录 | 内容与含义 |
|---|---|
| original_game_exports | 7 个 Skeleton Necromancer 原动作 PSA、原导出 props/config、配套骨架 glTF/bin。PSA 是 UE Viewer 从本机原游戏转换的导出格式，未冒称原 UE 原始容器。 |
| source_evidence | 完整原动作 JSON、19,721 个键的源字节/坐标核验、35 骨源 mesh 与 37 track 记录、技能时序、项目 Leviathan cast/rise 参考及格式实现依据。 |
| weapon_source | 项目既有蛇矛模型/贴图生成证据、原客户端 ItemModelGenerator 导出的几何和原 UV；不是重新设计的矛。 |
| adapted | 22 骨重定向、最终 8 clip payload/NPZ、获准握点刚体平移、最终整合输入、0.40 深色 palette 配置。 |
| validation | 最终 payload 数学核验、Blockbench 实际骨矩阵核验、独立保存文件握点/前刺核验，以及整合几何/纹理核验。 |
| scripts | 对应当前输入的 builder、importer、只读 validator、capture 和武器适配实现；不含连接凭据。 |

`source_evidence/animation_source_and_timing.md` 和 timing JSON 保留其生成时的来源研究状态；其中“尚未最终验收”是历史阶段说明。最终当前状态以 `FINAL_VALIDATION_INDEX.json`、本 README 和 validation 内对应哈希的报告为准；没有篡改来源研究文件来伪装成最终检查。

原动作并非不加改动地用于最终角色：walk 将原悬浮下肢改成双腿行走；attack 改成持蛇矛前刺并从立即生效姿态开始；strong 裁选原重击释放段；cast/rise 来自项目已有 Leviathan 动作并换骨框架；所有持物运动保留原手部跟随，同时移除不适合当前蛇矛的法杖 socket 位移。GetHitFront 保存为来源参考，不新增第九个交付动作。每个最终 clip 的 `source` 与 `notes` 均在 payload 内。

蛇矛唯一几何调整为统一刚体平移到真实握点，原 PNG、UV、形状、尺度和朝向不变；平移与语义握点见 `adapted/weapon_grip_alignment.json`。法袍 palette `[0.40,0.40,0.40]` 是用户授权风格变动：surface 与自然发光共用变暗 Albedo，辅助 S.B 的白色主发光不乘 palette；原 PNG 字节未改变。

## 最终验证摘要

- 实际 Blockbench 5.2.2 执行全部 536 个作者姿态并对比参考骨世界矩阵：PASS；最大旋转矩阵差 `1.176836406102666e-14`，最大位置差 `3.102051948644657e-11` Java 像素。
- 独立读取最终 bbmodel 的 8 clip，共 2724 个采样，覆盖全部存储 key、段中点与 120 Hz 网格：握点接触及绑定检查 PASS。
- attack 在 t=0 和 0.06 秒，握点到矛尖偏离 Java -Z 均为 0°，向前伸出约 20.4707083 像素。原矛尾到矛尖轴偏差约 0.24433°，源图案中心线与握点中心的定义不同，不混作同一测量。
- body/armor 坐标、UV 和原纹理保真；武器施加已授权 Δ 后逐点差 0，形状距离重算只有双精度残差。最终模型几何/骨/纹理/material 指纹 `09f0b3b31c9f8d25c46e6989f72a9685e2eeab844d49730a5989b39319bfa5f4`。

数值通过有明确范围：laugh 中握点纹素棱柱部分角可伸出手臂约 0.10959 像素，中心仍接触；walk 插值最低脚底可到约 -0.019186 像素，未声称连续严格贴地。有限采样不是全时域碰撞证明；native 骨矩阵验证也不是 Minecraft 实机、命中/伤害、清理生命周期或完整原 Unreal 渲染验证。

## 完整性和复现

`source_manifest.json` 记录每个文件的相对路径、分类、字节数与 SHA-256，复制前后逐字节哈希核对。7 个 PSA 还与先前导出清单中的 SHA-256 比较。本包最终 payload 和 NPZ 分别为 `4e614de79c7a37ebc0be235e86fb62eb82ca8abf2a1bd21e1c2538f92b81f017`、`a970b6b48e8a073d316bcd0d5d10ed3fb52755dc21b21f62b229db131c907ef5`；native 验证和独立 payload 核验均指向这两个最终输入。

脚本保留产生当前证据时的真实路径与导入约定，是可检查的实现快照，不声称任意目录解压即能无配置执行。运行导入/capture 需要本机 Blockbench MCP 会话，运行客户端提取需要用户本机 Java 客户端；这些凭据、完整客户端 JAR、classpath、编译 class、大 mappings、游戏 PAK 和密钥均未封装。脚本引用本项目已有 display_mob.py、Leviathan 工程和原绑定数据时保留原路径，dependencies 补存目标 bind 输入；未重复复制其他怪物完整工程。

原游戏模型/动画及源素材版权归 Mojang Studios / Microsoft 和相关权利人；本包只记录用户本地授权提取与项目适配，不赋予额外再分发权。UE Viewer 源码片段保持其原声明。未上传网络或打包完整游戏资源。
