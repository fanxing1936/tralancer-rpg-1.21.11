# 骨柱（as/at 骨柱，二阶段）
scoreboard players operation #m rpg_mk_i2 = #tick rpg_mk_i2
scoreboard players set #k rpg_mk_i2 300
scoreboard players operation #m rpg_mk_i2 %= #k rpg_mk_i2
execute if score #m rpg_mk_i2 matches 0 positioned ~ ~-2.3 ~ facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:michael_boss_i2/pillar/cast
