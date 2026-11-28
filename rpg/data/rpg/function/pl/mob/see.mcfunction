# 第一次见到这只怪（as/at 它）：本包召唤的（有名字或 NoAI）不动
tag @s add rpg.pl.s
execute if data entity @s CustomName run return 0
execute if entity @e[type=minecraft:marker,tag=rpg.pl.court,distance=..22] run return 0
execute store result score #np rpg_pl if entity @a[distance=..32,gamemode=!spectator]
execute if score #np rpg_pl matches 2 run attribute @s minecraft:max_health modifier add rpg:pl_party 0.4 add_multiplied_base
execute if score #np rpg_pl matches 3 run attribute @s minecraft:max_health modifier add rpg:pl_party 0.8 add_multiplied_base
execute if score #np rpg_pl matches 4 run attribute @s minecraft:max_health modifier add rpg:pl_party 1.2 add_multiplied_base
execute if score #np rpg_pl matches 5 run attribute @s minecraft:max_health modifier add rpg:pl_party 1.6 add_multiplied_base
execute if score #np rpg_pl matches 6 run attribute @s minecraft:max_health modifier add rpg:pl_party 2.0 add_multiplied_base
execute if score #np rpg_pl matches 7 run attribute @s minecraft:max_health modifier add rpg:pl_party 2.4 add_multiplied_base
execute if score #np rpg_pl matches 8.. run attribute @s minecraft:max_health modifier add rpg:pl_party 2.8 add_multiplied_base
execute if score #np rpg_pl matches 2.. run data modify entity @s Health set value 1024f
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=..160] run return run function rpg:pl/mob/z0
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=..240] run return run function rpg:pl/mob/z1
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=..560] run return run function rpg:pl/mob/z2
function rpg:pl/mob/z3
