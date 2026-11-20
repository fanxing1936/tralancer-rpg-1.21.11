# 骨柱（as/at 骨柱，二阶段）
scoreboard players operation #m rpg_mk = #tick rpg_mk
scoreboard players set #k rpg_mk 300
scoreboard players operation #m rpg_mk %= #k rpg_mk
execute if score #m rpg_mk matches 0 positioned ~ ~-2.3 ~ facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet rotated ~ 0 run function rpg:michael_boss/pillar/cast
