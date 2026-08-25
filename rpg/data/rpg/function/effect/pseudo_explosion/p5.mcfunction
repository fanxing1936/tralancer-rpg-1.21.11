# 伪爆炸：只有表现与伤害，不生成会改方块的爆炸实体。
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force
particle minecraft:large_smoke ~ ~0.4 ~ 1.1 1.1 1.1 0.08 37 force
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.845
execute as @e[distance=..5] if data entity @s Health run damage @s 20 minecraft:explosion at ~ ~ ~
execute as @e[distance=5.01..10] if data entity @s Health run damage @s 10 minecraft:explosion at ~ ~ ~
