# 原来的格子空着就放回去，否则掉在脚下（不会被别人捡走）
$execute unless items entity @s $(slot) * run return run item replace entity @s $(slot) from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] contents
execute at @s run summon minecraft:item ~ ~0.3 ~ {Tags:["rpg.dt.drop"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}
execute at @s run data modify entity @e[type=minecraft:item,tag=rpg.dt.drop,limit=1,sort=nearest] Item set from entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item
execute at @s run data modify entity @e[type=minecraft:item,tag=rpg.dt.drop,limit=1,sort=nearest] Owner set from entity @s UUID
tag @e[type=minecraft:item,tag=rpg.dt.drop] remove rpg.dt.drop
