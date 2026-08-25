tag @e[type=minecraft:item,tag=rpg.rite.tool.nail,distance=..4] remove rpg.rite.tool.nail
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run function rpg:inquest/tool/place/nail
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run tag @s add rpg.rite.nailed
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_stab 20
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1,scores={rpg_ex_stab=101..}] run scoreboard players set @s rpg_ex_stab 100
particle end_rod ~ ~0.2 ~ 0.35 0.1 0.35 0.02 30 force
playsound minecraft:block.anvil.place player @a[distance=..14] ~ ~ ~ 0.7 1.8
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[银质圣钉] ","color":"#DCE6EE","bold":true,"italic":false},{"text":"法阵边界已固定。","color":"gray","italic":false}]
