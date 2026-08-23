# 人偶身上多一道裂。10 点生命 = 能替你挡十轮，挡满就碎。
# 先看这一下是不是致命的那一下 —— 放在扣血之后判会早报一拍。
execute if entity @s[nbt={Health:1.0f}] run function rpg:doll/shatter
damage @s 1 minecraft:magic
particle sculk_soul ~ ~0.5 ~ 0.2 0.25 0.2 0.05 14
particle dust{color:[0.32,0.16,0.42],scale:1} ~ ~0.5 ~ 0.2 0.25 0.2 0.02 10
playsound minecraft:block.amethyst_block.break hostile @a[distance=..16] ~ ~ ~ 0.7 0.6
