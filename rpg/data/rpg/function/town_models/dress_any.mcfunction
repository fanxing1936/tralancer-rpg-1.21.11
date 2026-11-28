# 按载体实体类型和角色标签选取一套外观。
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.priest] run return run function rpg:town_models/town_priest/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.elder] run return run function rpg:town_models/town_elder/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.bard] run return run function rpg:town_models/town_bard/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.watchman] run return run function rpg:town_models/town_watchman/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.witch] run return run function rpg:town_models/town_witch/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.hood] run return run function rpg:town_models/town_edgewalker/dress
execute if entity @s[type=minecraft:vindicator,tag=rpg.te.inq] run return run function rpg:town_models/town_inquisitor/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmwife] run return run function rpg:town_models/town_folk_a/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmer] run return run function rpg:town_models/town_folk_b/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.lad] run return run function rpg:town_models/town_folk_c/dress
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.child] run return run function rpg:town_models/town_child/dress
execute if entity @s[type=minecraft:zombie,tag=rpg.te.big] run return run function rpg:town_models/town_hollow_big/dress
execute if entity @s[type=minecraft:zombie,tag=rpg.te.hol,tag=!rpg.te.big] run return run function rpg:town_models/town_hollow/dress
