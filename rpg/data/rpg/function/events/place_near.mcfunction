kill @e[type=minecraft:marker,tag=rpg.ev.mk]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.ev.mk"]}
spreadplayers ~ ~ 2 10 under 200 false @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1]
