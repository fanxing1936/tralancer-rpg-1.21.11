# 每秒（as/at 玩家）：开关式与定时的赐福
scoreboard players add @s rpg_pa_t 1
execute if score @s rpg_pa_t matches 60.. run scoreboard players set @s rpg_pa_t 0
scoreboard players operation #q rpg_pa = @s rpg_pa_t
scoreboard players operation #q rpg_pa %= #10 rpg_pa
execute if score @s rpg_ps_30 matches 2 if score #q rpg_pa matches 0 if predicate rpg:paths/day run effect give @s minecraft:regeneration 2 1 true
execute if score @s rpg_ps_31 matches 3 if score @s rpg_pa_tsd matches ..40 unless entity @s[tag=rpg.pa.rs] run effect give @s minecraft:resistance 10 0 true
execute if score @s rpg_ps_31 matches 3 if score @s rpg_pa_tsd matches ..40 run tag @s add rpg.pa.rs
execute if score @s rpg_pa_tsd matches 41.. run tag @s remove rpg.pa.rs
execute if score @s rpg_ps_29 matches 3 unless predicate rpg:paths/day run attribute @s minecraft:armor modifier add rpg:pa_29n 2 add_value
execute if score @s rpg_ps_29 matches 3 if predicate rpg:paths/day run attribute @s minecraft:armor modifier remove rpg:pa_29n
execute if score @s rpg_ps_26 matches 2 if score @s rpg_pa_t matches 0 if score @s rpg_taint matches 1.. run scoreboard players remove @s rpg_taint 1
execute if score @s rpg_ps_23 matches 2 run function rpg:paths/low_res
execute if score @s rpg_ps_17 matches 2 if items entity @s weapon.offhand * run attribute @s minecraft:armor modifier add rpg:pa_17o 2 add_value
execute if score @s rpg_ps_17 matches 2 unless items entity @s weapon.offhand * run attribute @s minecraft:armor modifier remove rpg:pa_17o
scoreboard players operation #q rpg_pa = @s rpg_pa_t
scoreboard players operation #q rpg_pa %= #30 rpg_pa
execute if score @s rpg_ps_16 matches 2 if score #q rpg_pa matches 0 if score @s rpg_force matches 1 run function rpg:paths/holy
execute if score @s rpg_ps_16 matches 2 if score #q rpg_pa matches 0 if score @s rpg_force matches 3 run function rpg:paths/holy
execute if score @s rpg_ps_11 matches 3 run function rpg:paths/xl
