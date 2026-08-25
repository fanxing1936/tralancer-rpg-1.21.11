# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 0.4 0.4 0.4 0.08 17 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 1.065
execute as @e[distance=..1] if data entity @s Health run damage @s 4 minecraft:explosion at ~ ~ ~
execute as @e[distance=1.01..2] if data entity @s Health run damage @s 2 minecraft:explosion at ~ ~ ~
