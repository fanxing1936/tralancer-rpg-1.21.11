# 时候到了，它自己散掉 —— 不是被你打退的。
#
# 先把探针一起收走：自己散掉的**不炸**，炸的只有被打死的。
execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 0.5 0.9 0.5 0.08 60
particle large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.05 40
particle squid_ink ~ ~1 ~ 0.4 0.8 0.4 0.05 30
playsound minecraft:entity.evoker.death hostile @a[distance=..32] ~ ~ ~ 1 0.6
kill @s
