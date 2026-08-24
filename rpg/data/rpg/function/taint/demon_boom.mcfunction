# 死亡爆炸。fuse:0 的 TNT 是同刻就炸的 —— 苦力怕点了火还要鼓 1.5 秒。
# 探针骑在乘客位上，比脚下高两格 —— 往下压一点，炸在身上而不是头顶
particle explosion_emitter ~ ~-1.2 ~ 0 0 0 0 1
particle sculk_soul ~ ~0.5 ~ 1 1 1 0.2 80
particle large_smoke ~ ~0.5 ~ 1 1 1 0.1 50
playsound minecraft:entity.wither.death hostile @a[distance=..48] ~ ~ ~ 1 0.7
summon minecraft:tnt ~ ~-1.2 ~ {fuse:0s,explosion_power:4.0f}
kill @s
