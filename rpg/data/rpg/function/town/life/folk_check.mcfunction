# 每 30 秒：附近有玩家的镇，农妇、农夫、少年缺谁补谁（as/at 镇中心标记）
scoreboard players operation #built rpg_tw = @s rpg_tw_id
execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.farmwife,distance=..200] run function rpg:town/life/folk_add_farmwife
execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.farmer,distance=..200] run function rpg:town/life/folk_add_farmer
execute unless entity @e[type=minecraft:villager,tag=rpg.tnpc.lad,distance=..200] run function rpg:town/life/folk_add_lad
