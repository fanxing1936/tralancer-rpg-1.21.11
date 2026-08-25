tag @s add rpg.rite.anchor.active
scoreboard players set @s rpg_ex_stage 4
scoreboard players set @s rpg_ex_time 300
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ransom 0
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/boss_stage4
title @a[distance=..14,gamemode=!spectator] times 5 40 15
title @a[distance=..14,gamemode=!spectator] title ["",{"text":"Ⅳ · 裁　决","color":"#FFF2A8","bold":true,"italic":false}]
title @a[distance=..14,gamemode=!spectator] subtitle ["",{"text":"选择恶魔离开此世的方式","color":"white","italic":false}]
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[罪约裁决] ","color":"#FFF2A8","italic":false,"bold":true},{"text":"为祂写下离开此世的结局。","color":"gray","italic":false}]
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[消灭]","color":"#FF6B5E","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 1"}},{"text":"  ","color":"white","italic":false},{"text":"[放逐]","color":"#FFF2A8","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 2"}},{"text":"  ","color":"white","italic":false},{"text":"[封印]","color":"#62D9E8","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 3"}},{"text":"  ","color":"white","italic":false},{"text":"[契约]","color":"#D596F2","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 4"}}]
playsound minecraft:block.end_portal.spawn player @a[distance=..28] ~ ~ ~ 0.8 1.5
tag @s remove rpg.rite.anchor.active
