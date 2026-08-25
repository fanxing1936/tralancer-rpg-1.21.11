# 死亡伪爆炸。探针骑在乘客位上，比脚下高两格 —— 往下压一点，
# 在降临者身上结算表现与伤害；不生成 TNT，也不修改任何方块。
particle sculk_soul ~ ~0.5 ~ 1 1 1 0.2 80
particle large_smoke ~ ~0.5 ~ 1 1 1 0.1 50
playsound minecraft:entity.wither.death hostile @a[distance=..48] ~ ~ ~ 1 0.7
execute positioned ~ ~-1.2 ~ run function rpg:effect/pseudo_explosion/p4
kill @s
