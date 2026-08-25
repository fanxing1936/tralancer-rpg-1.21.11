# 爆心 marker 只活在这次同步调用内：by=爆心保证击退方向，from=施法者保留归属。
kill @e[type=minecraft:marker,tag=rpg.pseudo_boom.center]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.pseudo_boom.center"]}
# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 0.66 0.66 0.66 0.08 27 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.955
execute as @e[distance=..3,tag=!rpg.pseudo_boom.source] if data entity @s Health run damage @s 12 minecraft:explosion by @e[type=minecraft:marker,tag=rpg.pseudo_boom.center,distance=..0.1,limit=1] from @e[tag=rpg.pseudo_boom.source,limit=1]
execute as @e[distance=3.01..6,tag=!rpg.pseudo_boom.source] if data entity @s Health run damage @s 6 minecraft:explosion by @e[type=minecraft:marker,tag=rpg.pseudo_boom.center,distance=..0.1,limit=1] from @e[tag=rpg.pseudo_boom.source,limit=1]
kill @e[type=minecraft:marker,tag=rpg.pseudo_boom.center,distance=..0.1]
