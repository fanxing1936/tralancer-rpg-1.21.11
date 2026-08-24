# 探针还骑在主人身上吗？骑着就有 vehicle；主人一死，它被当场甩下来。
scoreboard players set #ride rpg_fall 0
execute on vehicle run scoreboard players set #ride rpg_fall 1
execute if score #ride rpg_fall matches 0 at @s run function rpg:taint/demon_boom
