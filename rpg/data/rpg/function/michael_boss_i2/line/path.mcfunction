tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.mkb.hit
scoreboard players remove #d rpg_mk_i2 1
execute if score #d rpg_mk_i2 matches 1.. positioned ^ ^ ^1.5 run function rpg:michael_boss_i2/line/path
