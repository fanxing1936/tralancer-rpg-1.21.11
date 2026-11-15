execute if entity @s[tag=rpg.jqb.a5] positioned ~ ~-0.9 ~ as @e[tag=rpg.unit.f,distance=..1.2,limit=1,sort=nearest] run damage @s 5 minecraft:mob_projectile by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute if entity @s[tag=rpg.jqb.a6] positioned ~ ~-0.9 ~ as @e[tag=rpg.unit.f,distance=..1.2,limit=1,sort=nearest] run damage @s 6 minecraft:mob_projectile by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
function rpg:jacques_boss/fx/arrow_end
