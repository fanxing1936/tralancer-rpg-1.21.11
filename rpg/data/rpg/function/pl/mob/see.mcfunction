# 第一次见到这只怪（as/at 它）：本包召唤的（有名字或 NoAI）不动
tag @s add rpg.pl.s
execute if data entity @s CustomName run return 0
execute if entity @e[type=minecraft:marker,tag=rpg.pl.court,distance=..22] run return 0
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=..240] run return run function rpg:pl/mob/z1
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=..560] run return run function rpg:pl/mob/z2
function rpg:pl/mob/z3
