execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id run return run function rpg:campaign/beelzebub/rite/collapse
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[仪式失败] ","color":"dark_red","bold":true,"italic":false},{"text":"稳定度归零，裁决被迫写为——消灭。","color":"gray","italic":false}]
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/eliminate_boss
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
function rpg:inquest/tool/cleanup
particle explosion_emitter ~ ~0.8 ~ 0 0 0 0 1 force
playsound minecraft:block.beacon.deactivate hostile @a[distance=..28] ~ ~ ~ 1 0.45
kill @s
