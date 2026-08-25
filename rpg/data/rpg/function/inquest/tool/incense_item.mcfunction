tag @e[type=minecraft:item,tag=rpg.rite.tool.incense,distance=..4] remove rpg.rite.tool.incense
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run function rpg:inquest/tool/place/incense
function rpg:inquest/tool/consume
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_toolcd 200
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..3,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_stab 15
effect clear @a[distance=..6,gamemode=!spectator] minecraft:slowness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:weakness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:blindness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:darkness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:nausea
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:strength 8 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:speed 8 1 true
particle campfire_cosy_smoke ~ ~0.4 ~ 1.2 0.3 1.2 0.03 35 force
tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[净罪香] ","color":"#E7D7B5","bold":true,"italic":false},{"text":"污秽暂退，恶魔因香火而狂怒。","color":"gray","italic":false}]
