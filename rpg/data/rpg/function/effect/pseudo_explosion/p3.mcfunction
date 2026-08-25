# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 0.66 0.66 0.66 0.08 27 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.955
execute as @e[distance=..3] if data entity @s Health run damage @s 12 minecraft:explosion at ~ ~ ~
execute as @e[distance=3.01..6] if data entity @s Health run damage @s 6 minecraft:explosion at ~ ~ ~
