scoreboard players set @s rpg_mer_hoe 0
loot give @s loot rpg:world/currency
execute as @e[tag=rpg.mer,distance=..6,limit=1,sort=nearest] at @s run particle minecraft:angry_villager ~ ~2 ~ 0.3 0.2 0.3 0 6
execute if entity @e[tag=rpg.mer.temp,distance=..6] run function rpg:events/end
function rpg:quest/title/get_merchant
