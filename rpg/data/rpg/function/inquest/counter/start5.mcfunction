execute if entity @s[tag=rpg.rite.nailed] run return run function rpg:inquest/counter/samael_blocked
function rpg:inquest/stability/hit25
tag @s add rpg.rite.anchor.active
execute as @a[distance=..7,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] feet run tp @s ^ ^0.25 ^-1.4
tag @s remove rpg.rite.anchor.active
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:1.5} ~2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:1.5} ~-2 ~0.1 ~ 0.2 0.1 2 0.02 35 force
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:1.5} ~ ~0.1 ~2 2 0.1 0.2 0.02 35 force
particle dust_color_transition{from_color:[1.0,0.36,0.32],to_color:[0.48,0.14,0.11],scale:1.5} ~ ~0.1 ~-2 2 0.1 0.2 0.02 35 force
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"〖反仪式・暴怒〗","color":"#C4433A","bold":true,"italic":false},{"text":" 𝔚𝔯𝔞𝔱𝔥","color":"#7F2C26","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"萨麦尔击碎法阵边缘并震开守阵者。","color":"#9C9A94","italic":false}]
