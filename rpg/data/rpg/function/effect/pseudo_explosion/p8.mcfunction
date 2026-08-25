# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 1.76 1.76 1.76 0.08 52 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.68
execute as @e[distance=..8] if data entity @s Health run damage @s 32 minecraft:explosion at ~ ~ ~
execute as @e[distance=8.01..16] if data entity @s Health run damage @s 16 minecraft:explosion at ~ ~ ~
