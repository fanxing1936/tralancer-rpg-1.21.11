execute unless entity @e[type=minecraft:interaction,tag=rpg.bench,distance=..0.2] run summon minecraft:interaction ~ ~ ~ {Tags:["rpg.bench"],width:1.02f,height:0.5f,response:1b}
scoreboard players set @e[type=minecraft:interaction,tag=rpg.bench,distance=..0.2] rpg_bn 6
