# 以这位迷途商人为执行者播放 look。
execute unless entity @s[type=minecraft:villager,tag=rpg.mer.model.travel] run return 0
execute at @s run function rpg:merchant_travel/anim/enter/look
