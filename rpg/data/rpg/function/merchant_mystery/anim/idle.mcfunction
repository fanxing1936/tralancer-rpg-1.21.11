# 以这位神秘商人为执行者播放 idle。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.mystery] run return 0
execute at @s run function rpg:merchant_mystery/anim/enter/idle
