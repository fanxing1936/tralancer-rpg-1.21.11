# 教皇 M4 专用服务端运行时验证

功能断言 **155 / 155 通过**，函数/命令错误 **0**，服务端正常退出（退出码 0）。
保留 **1 条准备阶段性能 WARN**，因此 `functional_success=true`，而
`success=false`、`strict_success=false`。这两个判定没有混为“全部无警告”。

## 测试对象与结果

- Minecraft Java 1.21.11 真实专用服务端，监听 `127.0.0.1:25675`；没有启动客户端。
- 来源：`_pope_m4_qa_20261105/build_1793851086149543000/rpg`。
- 模型 SHA-256：`a419cc8dce1e796113a02c362ad184faea3bf09d5c908b26ac81e963babc624a`。
- 新建世界：`_pope_m4_qa_20261105/server_runtime_1793851298979/packtest`。
- 召唤检查：卫道士载体、初始生命值/最大生命值 1000、12 个 item_display、12 个真实乘客。
- 实测全部乘客 `PosY - carrier.PosY = 2.0`，符合普通 scale=1 卫道士座高。
- 清除隐身后，下一服务器刻由 `tick_late` 恢复隐身。
- 九段动画编号、首/中/末帧、循环周期、非循环结束回 idle 均通过。
- 40 组实际实体目标变换检查覆盖 480 个部件结果；相对烘焙目标最大数值误差
  `1.375184366381177e-7`，阈值 `1e-6`，旋转按四元数正规化后比较。
- 两个主世界实例、一个下界实例、一个末地实例独立播放不同片段，每服务器刻只推进一次。
- 仅 `kill` 载体，等待 23 刻覆盖载体死亡阶段；三个原版维度已加载区块均无残留部件。
- 未写玩家实例；只复用已有的 `eula=true` 文件，原文件哈希未改变。

完整断言和实际数值见 [report.json](report.json)，原始控制台见 [console.log](console.log)。

## 唯一性能警告的发生位置

原文（[console.log](console.log) 第 41 行）：

```text
[12:01:54] [Server thread/WARN]: Can't keep up! Is the server overloaded? Running 2301ms or 46 ticks behind
```

该时刻已执行 `tick freeze`，刚开始为新世界强制加载下界/末地区块；首个
`function rpg:pope/summon` 在第 **61** 行，晚于警告。首次召唤后载体总数为 1 的断言通过。
这些证据表明警告发生在模型测试准备阶段，未进入九段动作验证阶段。
没有在 WARN 当刻直接查询“零实体”，不能把时序证据说成当刻实体快照。

脚本没有过滤这条 WARN：它仍在 `unexpected_warnings`，并额外记入
`setup_performance_warnings`，含发生行号、首个召唤行号和证据边界。
另外四条标准本机离线模式通知逐条保存在 `known_environment_warnings`。
本次不是性能基准测试，不据此宣称所有运行场景都不会卡顿。

## 隔离控制与验证范围

完整构建数据包被复制进全新测试世界；仅该一次性副本的 tick tag 删除
`rpg:pope_fight/tick` 注册，所有玩法函数仍由服务端解析加载。
原始/测试 tick tag 哈希和删除项均写入 `test_controls`，源包未改。
完整包未经裁剪的 `server_test.py` 冒烟验证由 M4 另一份报告提供。

测试给载体临时设置 `NoAI`、`NoGravity`，在冻结状态下按普通 20 TPS 精确推进；
walk 测试每四刻水平移动 0.25 格，并重设初始移动检测相位。
这些只是测试夹具，生成器没有因此加入战斗 AI、技能或阶段逻辑。
本报告证明模型运行时接口，**不证明完整教皇战的动作调度兼容性**。

## 修复过的真实问题

第一轮发现三维入口中无空间条件的 `@e` 会跨维度选中载体，导致每刻推进三次。
五刻后的实际 attack 身体位移逐值等于旧烘焙 f15；第一轮 155 项中仅 85 项通过。
失败报告、日志和定位证据保存在 [attempt1_threefold_tick](attempt1_threefold_tick/diagnosis.json)。

修复只落在教皇生成器的 `tick_dimension` 和 `tick_late`，给选择器加入
`distance=0..` 限定当前维度；没有修改 `display_mob.py`。
完整新快照重建后进行本轮验证，155 项全部通过。第二轮原始严格判定报告另存于
[attempt2_strict_original/report.json](attempt2_strict_original/report.json)，后续只补充分级说明，没有再次运行或删除警告。

## 尚未验证

**未在真实游戏内看过。** 实体目标 NBT 不等于客户端插值姿势；本次没有验证
客户端视觉还原、半透明排序、发光观感或实际音效听感。
孤儿清理结论仅针对本次已加载区块，不覆盖卸载区块或自定义维度。

