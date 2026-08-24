# 降临者的一刻：寿命，以及他自己那一手。
# 场上没有这样的东西时，上层那道守卫会整段跳过。

# 没上过发条的先上发条 —— **不要**把它当成过期。
#
# 寿命是 advent_life 给的；任何一条召唤路径漏掉那一步（手抄一条 summon、
# 旧存档里遗留的实体、别处复制过去的 NBT……），它一进这里 rpg_fall 就是 0，
# 于是当场被自己人清掉 —— 表现就是"召唤出来立刻死"。
# 这一行把那条路堵死：认不出发条，就补一个，而不是判死刑。
execute if entity @s[tag=!rpg.advent.timed] run function rpg:taint/advent_arm

scoreboard players remove @s rpg_fall 1
execute if entity @s[scores={rpg_fall=..0}] at @s run return run function rpg:taint/advent_gone

# 出手。scores= 只认已经存在的分数，所以先把冷却坐实。
scoreboard players add @s rpg_dm_cd 0
execute if entity @s[scores={rpg_dm_cd=1..}] run return run scoreboard players remove @s rpg_dm_cd 1
execute at @s if entity @a[distance=..12,gamemode=!spectator,gamemode=!creative] run function rpg:taint/cast
