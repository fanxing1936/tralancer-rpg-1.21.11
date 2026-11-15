tag @e[tag=rpg.unit.f,distance=..1.6] add rpg.jqb.hit
scoreboard players remove #d rpg_jq 1
execute if score #d rpg_jq matches 1.. positioned ^ ^ ^1.5 run function rpg:jacques_boss/line/wide
