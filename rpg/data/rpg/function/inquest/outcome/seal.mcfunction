execute if entity @s[tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_ch1_id if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.ch1.boss,tag=rpg.exorcism.bound,distance=..14,sort=nearest,limit=1] rpg_rite_id run return run function rpg:campaign/beelzebub/verdict/seal
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run function rpg:inquest/outcome/seal_boss
tellraw @a[distance=..20,gamemode=!spectator] ["",{"text":"[裁决·封印] ","color":"#62D9E8","bold":true,"italic":false},{"text":"残魂已收入封魔灯；封印并非永恒。","color":"gray","italic":false}]
particle soul_fire_flame ~ ~0.8 ~ 1.1 0.6 1.1 0.08 80 force
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.4
function rpg:inquest/tool/cleanup
kill @s
