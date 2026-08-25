tag @e[type=minecraft:item,tag=rpg.rite.tool.chalk2,distance=..4] remove rpg.rite.tool.chalk2
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run function rpg:inquest/tool/place/chalk2
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run tag @s add rpg.layout.suppress
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players remove @s rpg_ex_slots 1
particle dust{color:[0.72,0.86,1.0],scale:0.8} ~ ~0.15 ~ 1.8 0.05 1.8 0.01 45 force
playsound minecraft:block.calcite.place player @a[distance=..14] ~ ~ ~ 0.8 1.4
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[仪式粉笔] ","color":"#C8B6E8","bold":true,"italic":false},{"text":"压制法阵已刻写。","color":"gray","italic":false}]
