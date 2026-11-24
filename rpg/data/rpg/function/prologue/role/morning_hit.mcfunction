# 一颗坠星（as/at 被击中的敌人）
particle minecraft:end_rod ~ ~4 ~ 0.05 2 0.05 0.02 12
particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1
damage @s 12 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
