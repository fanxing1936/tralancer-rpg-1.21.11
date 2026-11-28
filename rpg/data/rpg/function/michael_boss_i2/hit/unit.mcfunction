# 他被打到（as/at 他；攻击者带 rpg.mkb.att）
execute if entity @s[tag=rpg.mkb.end] run return 0
execute if entity @s[tag=rpg.mkb.morph] run return 0
execute if entity @s[tag=rpg.mkb.solid] run return run scoreboard players set @e[tag=rpg.unit,tag=rpg.mkb.att,distance=0..] rpg_mk_v 3
execute if entity @s[tag=rpg.mkb.fold] run return run function rpg:michael_boss_i2/hit/fold
execute if score #w rpg_mk_i2 matches 1.. run scoreboard players set @e[tag=rpg.unit,tag=rpg.mkb.att,distance=0..] rpg_mk_v 4
