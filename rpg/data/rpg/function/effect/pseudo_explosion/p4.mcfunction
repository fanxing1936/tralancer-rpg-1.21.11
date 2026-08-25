# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 0.88 0.88 0.88 0.08 32 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.9
execute as @e[distance=..4] if data entity @s Health run damage @s 16 minecraft:explosion at ~ ~ ~
execute as @e[distance=4.01..8] if data entity @s Health run damage @s 8 minecraft:explosion at ~ ~ ~
