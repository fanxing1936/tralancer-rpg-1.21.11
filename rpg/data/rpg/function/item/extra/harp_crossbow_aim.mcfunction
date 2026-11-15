# 新补的这支箭：速度与原版弩箭相同，归属记在射手名下（击杀、掉落都算他的）
execute store result entity @s Motion[0] double 0.003150 run scoreboard players get #dx rpg_hc_tmp
execute store result entity @s Motion[1] double 0.003150 run scoreboard players get #dy rpg_hc_tmp
execute store result entity @s Motion[2] double 0.003150 run scoreboard players get #dz rpg_hc_tmp
data modify entity @s Owner set from entity @a[tag=rpg.hc.cast,limit=1] UUID
tag @s remove rpg.hc.new
