# 此刻 @s 是攻击者，受击者由上一层的同步标签精确锁定。
effect give @e[tag=rpg.samael.victim,distance=..1,limit=1] minecraft:poison 6 1 true
particle dust{color:[0.69,0.0,0.34],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
