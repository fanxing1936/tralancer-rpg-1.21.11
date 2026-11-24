# as/at 主持玩家：在 16~40 格外的地面上放事件标记
kill @e[type=minecraft:marker,tag=rpg.ev.mk]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.ev.mk"]}
spreadplayers ~ ~ 4 28 under 200 false @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1]
