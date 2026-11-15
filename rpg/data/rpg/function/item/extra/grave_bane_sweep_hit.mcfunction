# 被横扫扫到的一个。亡灵受伤加倍左右。
particle dust{color:[1.0,0.85,0.35],scale:0.7} ~ ~1 ~ 0.25 0.35 0.25 0 5
execute if entity @s[type=#minecraft:undead] run return run damage @s 14 rpg:grave_sweep by @a[tag=rpg.gb.cast,limit=1]
damage @s 8 rpg:grave_sweep by @a[tag=rpg.gb.cast,limit=1]
