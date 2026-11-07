# 判定体只会被一击打穿才没有；正常死亡走血量。
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1] run return run function rpg:pope_fight/heart/die
execute as @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1] at @s run function rpg:pope_fight/heart/tick
