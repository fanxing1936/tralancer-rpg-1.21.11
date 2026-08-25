
# 只结算属于当前 Boss 唯一 id 的二阶段侍从。第一行的距离仅用于给升级前
# 没有 id 的近身旧侍从补归属；已有 id 后即使追出十二格，也会按时收尾。
tag @e[tag=rpg.pseudo_boom.source] remove rpg.pseudo_boom.source
tag @s add rpg.pseudo_boom.source
execute as @e[type=minecraft:vindicator,tag=devil2,tag=tick,distance=..12] unless score @s rpg_boom_id matches 1.. run scoreboard players operation @s rpg_boom_id = @e[tag=rpg.pseudo_boom.source,limit=1] rpg_boom_id
execute if entity @e[type=minecraft:vindicator,tag=devil2,tag=tick] run function rpg:entities/warden/pseudo_burst_minions/g0
tag @s remove rpg.pseudo_boom.source
