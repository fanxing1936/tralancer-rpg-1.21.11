execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 每秒：失明别掉，人别飘走
execute unless entity @s[tag=rpg.ob.hold] run return 0
gamemode spectator @s
effect give @s minecraft:blindness infinite 0 true
execute unless entity @s[y=315,dy=2] run function rpg:onboard/hold/tp_go with storage rpg:onboard tmp
