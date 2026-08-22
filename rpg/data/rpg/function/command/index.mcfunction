# Auto-generated per-tick flag index.
# 每个族群只遍历一次：清标记与判定都在 @s 上完成，
# 于是玩家表每刻只走一遍、掉落物表也只走一遍。

execute as @a run function rpg:command/index_player
execute as @e[type=minecraft:item] run function rpg:command/index_item

## damage detection
tag @e[tag=rpg.hurt] remove rpg.hurt
execute as @a at @s run function rpg:command/damage_scan
