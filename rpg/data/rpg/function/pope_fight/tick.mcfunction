# 每刻入口：没开战时只有这一条分数判定。特效都活不过战斗，clear 会收走。
execute unless score #stage rpg_pf matches 1.. run return 0
execute if entity @e[tag=rpg.pope.fx,limit=1] run function rpg:pope_fight/fx/tick
execute as @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] at @s run return run function rpg:pope_fight/run
function rpg:pope_fight/clear
