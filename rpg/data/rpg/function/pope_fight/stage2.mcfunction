# 他倒下有两条路：血量到线，或一击打穿。后者靠这条兜底。
execute unless entity @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] run return run function rpg:pope_fight/stage3_enter
execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1] at @s run function rpg:pope_fight/boss/tick
