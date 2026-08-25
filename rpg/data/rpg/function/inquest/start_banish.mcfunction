tag @s add rpg.rite.anchor.active
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 40
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_stage4
title @a[distance=..14,gamemode=!spectator] times 5 35 15
title @a[distance=..14,gamemode=!spectator] title ["",{"text":"Ⅳ · 逐　离","color":"#FFF2A8","bold":true,"italic":false}]
title @a[distance=..14,gamemode=!spectator] subtitle ["",{"text":"法阵闭合 · 此世拒绝其名","color":"white","italic":false}]
playsound minecraft:block.end_portal.spawn player @a[distance=..28] ~ ~ ~ 0.8 1.5
tag @s remove rpg.rite.anchor.active
