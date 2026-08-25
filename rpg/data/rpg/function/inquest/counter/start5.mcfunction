execute if entity @s[tag=rpg.rite.nailed] run return run function rpg:inquest/counter/samael_blocked
function rpg:inquest/stability/hit25
tag @s add rpg.rite.anchor.active
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^0.25 ^-1.4
tag @s remove rpg.rite.anchor.active
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~-2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~ ~0.1 ~2 2 0.1 0.2 0.02 35 force
particle dust{color:[1.0,0.12,0.08],scale:1.5} ~ ~0.1 ~-2 2 0.1 0.2 0.02 35 force
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[反仪式·暴怒] ","color":"#FF7A70","bold":true,"italic":false},{"text":"萨麦尔击碎法阵边缘并震开守阵者。","color":"gray","italic":false}]
