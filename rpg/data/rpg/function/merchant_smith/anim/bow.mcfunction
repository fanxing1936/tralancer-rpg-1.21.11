# 以这位铁匠为执行者播放 bow。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.smith] run return 0
execute at @s run function rpg:merchant_smith/anim/enter/bow
execute at @s run playsound minecraft:entity.villager.trade neutral @a[distance=..16] ~ ~ ~ 1 1
