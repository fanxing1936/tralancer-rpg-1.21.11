# 他被打到（as/at 他；攻击者带 rpg.slb.att）：判定这一下怎么算，记在攻击者的 rpg_sl_v 上。
execute if entity @s[tag=rpg.slb.end] run return 0
execute if entity @s[tag=rpg.slb.morph] run return 0
tag @s remove rpg.slb.front
execute positioned ^ ^ ^2 if entity @e[tag=rpg.unit,tag=rpg.slb.att,distance=..3.2] run tag @s add rpg.slb.front
execute if entity @s[tag=rpg.slb.guard,tag=rpg.slb.front] run return run function rpg:saul_boss/hit/parry
execute if score @s rpg_sl matches 1 if entity @s[tag=rpg.slb.front] if predicate rpg:saul_boss/stalwart run return run function rpg:saul_boss/hit/negate
execute if entity @s[tag=rpg.slb.weak] run scoreboard players set @e[tag=rpg.unit,tag=rpg.slb.att] rpg_sl_v 3
