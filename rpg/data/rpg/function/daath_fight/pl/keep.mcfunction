# 还没复活：掉落物不许消失
execute if entity @s[tag=rpg.dt.kept] run return 0
tag @s add rpg.dt.kept
execute in rpg:daath as @e[type=minecraft:item,distance=0..] run data merge entity @s {Age:-32768s}
