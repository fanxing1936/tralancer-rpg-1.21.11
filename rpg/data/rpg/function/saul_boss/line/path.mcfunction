tag @e[tag=rpg.unit.f,distance=..1.4] add rpg.slb.hit
scoreboard players remove #d rpg_sl 1
execute if score #d rpg_sl matches 1.. positioned ^ ^ ^1.5 run function rpg:saul_boss/line/path
