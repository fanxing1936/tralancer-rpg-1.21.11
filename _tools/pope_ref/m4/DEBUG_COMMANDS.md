# 教皇模型调试命令

这些命令用于已同步模型的数据包与资源包。当前尚未同步测试实例。只测试模型，不启动 pope_fight。

1. 重载数据包 `/reload`，资源包用 F3+T 重载。
2. 在空地召唤 `/function rpg:pope/summon`。自然卫道士有原版行为；下面的 NoAI/NoGravity 只作手动模型审阅夹具，不属于生成器或战斗设计。

```mcfunction
/execute as @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] run data merge entity @s {NoAI:1b,NoGravity:1b}
/execute as @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] at @s run function rpg:pope/anim/enter/attack
```

把最后的 attack 换成 idle、walk、summon、cast、appear、teleport_in、teleport_out、whirlwind 即可。walk 只在载体移动时保持循环；静止时共用位移监测会在下一次检测后切回 idle。需要四面看头眼、肩臂、袍背、皇冠和权杖；特别检查 attack 杖头近地处、cast 浮动杖头、whirlwind 掉冠脱手及7秒末姿。

读取当前动画编号、计数器及部件：

```mcfunction
/scoreboard players get @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] rpg_pp_anim
/scoreboard players get @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] rpg_pp_t
/data get entity @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] Passengers
```

单独测试声音（其余事件见 sounds.json 的 pope.*）：

```mcfunction
/playsound rpg:pope.spell hostile @s ~ ~ ~ 1 1
/stopsound @s hostile rpg:pope.whirlwind
```

清理测试：只杀附近教皇载体，等待至少 2 秒，再检查附近部件。不要先杀部件，否则无法检验孤儿清理。

```mcfunction
/kill @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16]
/execute unless entity @e[type=minecraft:item_display,tag=rpg.pope.part,distance=..32] run say 教皇部件已清理
```

服务端已验证主世界、下界、末地的已加载区块；客户端仍须真实截图核对。瞬移不会自行透明/消失，旋风也不会自行变成末影之心，均由玩法后续交接。
