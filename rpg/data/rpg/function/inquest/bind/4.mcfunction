scoreboard players add #rite_next rpg_rite_id 1
scoreboard players operation @s rpg_rite_id = #rite_next rpg_rite_id
scoreboard players set @s rpg_ex_stage 2
tag @s add rpg.exorcism.bound
tag @s add rpg.exorcism.visible
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.totem.lit,tag=!rpg.totem.inv,tag=!rpg.rite.anchor,distance=..8,limit=1,sort=nearest] at @s run function rpg:inquest/anchor_bind/4
tag @s remove rpg.rite.subject
function rpg:inquest/phase2/shockwave
title @a[distance=..18,gamemode=!spectator] times 10 60 15
title @a[distance=..18,gamemode=!spectator] title ["",{"text":"Ⅱ · 镇　魔","color":"#5A6B1E","bold":true,"italic":false}]
title @a[distance=..18,gamemode=!spectator] subtitle ["",{"text":"别西卜 · 真名已被法阵承认","color":"#5A6B1E","italic":false}]
tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"[显形] ","color":"#5A6B1E","bold":true,"italic":false},{"text":"稳定度 50 / 100 · 右键布下弱点媒介：","color":"gray","italic":false},{"text":"毒马铃薯 · 腐宴残食","color":"white","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.25
