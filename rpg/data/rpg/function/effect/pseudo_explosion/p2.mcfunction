# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 0.44 0.44 0.44 0.08 22 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 1.01
execute as @e[distance=..2] if data entity @s Health run damage @s 8 minecraft:explosion at ~ ~ ~
execute as @e[distance=2.01..4] if data entity @s Health run damage @s 4 minecraft:explosion at ~ ~ ~
