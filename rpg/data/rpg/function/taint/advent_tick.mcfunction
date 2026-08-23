# 降临者的一刻：寿命，以及他自己那一手。
# 场上没有这样的东西时，上层那道守卫会整段跳过。
scoreboard players remove @s rpg_fall 1
execute if entity @s[scores={rpg_fall=..0}] at @s run return run function rpg:taint/advent_gone

# 出手。scores= 只认已经存在的分数，所以先把冷却坐实。
scoreboard players add @s rpg_dm_cd 0
execute if entity @s[scores={rpg_dm_cd=1..}] run return run scoreboard players remove @s rpg_dm_cd 1
execute at @s if entity @a[distance=..12,gamemode=!spectator,gamemode=!creative] run function rpg:taint/cast
