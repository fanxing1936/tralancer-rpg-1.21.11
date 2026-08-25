execute unless entity @s[tag=rpg.rite.nailed] run function rpg:inquest/stability/hit15
tag @s add rpg.rite.anchor.active
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^-1.8
execute if entity @s[tag=rpg.rite.nailed] as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^ ^0.8
tag @s remove rpg.rite.anchor.active
effect give @a[distance=..10,gamemode=!spectator] minecraft:nausea 5 0 true
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·色欲] ","color":"#D596F2","bold":true,"italic":false},{"text":"贝利尔诱使守阵者背离法阵中心。","color":"gray","italic":false}]
playsound minecraft:entity.allay.ambient_with_item hostile @a[distance=..20] ~ ~ ~ 1 0.45
