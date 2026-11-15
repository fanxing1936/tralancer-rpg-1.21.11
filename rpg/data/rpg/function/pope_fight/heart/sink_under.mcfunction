# 在地下换位置：这段时间打不到，也算不上恶魔。
data merge entity @s {Invulnerable:1b}
tag @s remove rpg.demon
execute at @e[tag=rpg.unit,tag=rpg.pf.tgt,limit=1] rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves facing entity @e[tag=rpg.unit,tag=rpg.pf.tgt,limit=1] feet rotated ~ 0 run function rpg:pope_fight/heart/sink_place
