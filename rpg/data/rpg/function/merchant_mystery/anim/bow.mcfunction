# 以这位神秘商人为执行者播放 bow。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.mystery] run return 0
execute at @s run function rpg:merchant_mystery/anim/enter/bow
execute at @s run playsound minecraft:entity.villager.trade neutral @a[distance=..16] ~ ~ ~ 1 1
