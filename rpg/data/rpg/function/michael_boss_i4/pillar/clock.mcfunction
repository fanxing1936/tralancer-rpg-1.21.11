# 骨柱（as/at 骨柱，二阶段）
scoreboard players operation #m rpg_mk_i4 = #tick rpg_mk_i4
scoreboard players set #k rpg_mk_i4 300
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 positioned ~ ~-2.3 ~ facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:michael_boss_i4/pillar/cast
