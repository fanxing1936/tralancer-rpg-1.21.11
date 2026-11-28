# 镇民（as 被点的镇民 or 玩家，#t 镇号）说一句今天的风声
scoreboard players set #k rpg_te 0
execute if score #t rpg_tl matches 1 run scoreboard players operation #k rpg_te = #ev1 rpg_te
execute if score #t rpg_tl matches 2 run scoreboard players operation #k rpg_te = #ev2 rpg_te
execute if score #t rpg_tl matches 3 run scoreboard players operation #k rpg_te = #ev3 rpg_te
execute if score #t rpg_tl matches 4 run scoreboard players operation #k rpg_te = #ev4 rpg_te
execute if score #t rpg_tl matches 5 run scoreboard players operation #k rpg_te = #ev5 rpg_te
execute if score #t rpg_tl matches 6 run scoreboard players operation #k rpg_te = #ev6 rpg_te
execute if score #t rpg_tl matches 7 run scoreboard players operation #k rpg_te = #ev7 rpg_te
execute if score #t rpg_tl matches 8 run scoreboard players operation #k rpg_te = #ev8 rpg_te
execute if score #t rpg_tl matches 9 run scoreboard players operation #k rpg_te = #ev9 rpg_te
execute if score #t rpg_tl matches 10 run scoreboard players operation #k rpg_te = #ev10 rpg_te
execute if score #t rpg_tl matches 11 run scoreboard players operation #k rpg_te = #ev11 rpg_te
execute if score #t rpg_tl matches 12 run scoreboard players operation #k rpg_te = #ev12 rpg_te
execute if score #t rpg_tl matches 13 run scoreboard players operation #k rpg_te = #ev13 rpg_te
execute if score #t rpg_tl matches 14 run scoreboard players operation #k rpg_te = #ev14 rpg_te
execute if score #t rpg_tl matches 15 run scoreboard players operation #k rpg_te = #ev15 rpg_te
execute if score #t rpg_tl matches 16 run scoreboard players operation #k rpg_te = #ev16 rpg_te
execute if score #t rpg_tl matches 17 run scoreboard players operation #k rpg_te = #ev17 rpg_te
execute if score #t rpg_tl matches 18 run scoreboard players operation #k rpg_te = #ev18 rpg_te
execute if score #t rpg_tl matches 19 run scoreboard players operation #k rpg_te = #ev19 rpg_te
execute if score #t rpg_tl matches 20 run scoreboard players operation #k rpg_te = #ev20 rpg_te
execute if entity @s[type=minecraft:villager] run scoreboard players set #folk rpg_tl 0
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmwife] run scoreboard players set #folk rpg_tl 1
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.farmer] run scoreboard players set #folk rpg_tl 2
execute if entity @s[type=minecraft:villager,tag=rpg.tnpc.lad] run scoreboard players set #folk rpg_tl 3
execute if score #k rpg_te matches 1 if score #folk rpg_tl matches 1 run return run function rpg:town/ev/r/k1_f1
execute if score #k rpg_te matches 1 if score #folk rpg_tl matches 2 run return run function rpg:town/ev/r/k1_f2
execute if score #k rpg_te matches 1 if score #folk rpg_tl matches 3 run return run function rpg:town/ev/r/k1_f3
execute if score #k rpg_te matches 2 if score #folk rpg_tl matches 1 run return run function rpg:town/ev/r/k2_f1
execute if score #k rpg_te matches 2 if score #folk rpg_tl matches 2 run return run function rpg:town/ev/r/k2_f2
execute if score #k rpg_te matches 2 if score #folk rpg_tl matches 3 run return run function rpg:town/ev/r/k2_f3
execute if score #k rpg_te matches 3 if score #folk rpg_tl matches 1 run return run function rpg:town/ev/r/k3_f1
execute if score #k rpg_te matches 3 if score #folk rpg_tl matches 2 run return run function rpg:town/ev/r/k3_f2
execute if score #k rpg_te matches 3 if score #folk rpg_tl matches 3 run return run function rpg:town/ev/r/k3_f3
execute if score #k rpg_te matches 0 if score #folk rpg_tl matches 2 run return run function rpg:town/ev/r/k0_f2
