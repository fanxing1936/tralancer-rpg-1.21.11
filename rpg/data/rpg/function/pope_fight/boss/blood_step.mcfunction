particle dust{color:[1.000f,0.847f,0.353f],scale:1.0} ~ ~ ~ 0 0 0 0 1 normal
scoreboard players add #d rpg_pf 1
# 瞄的是眼睛，距离却从脚下算，所以这里先降到脚边再比。
execute positioned ~ ~-1.6 ~ if entity @e[type=minecraft:vindicator,tag=rpg.pf.sac,distance=..1] run return 0
execute if score #d rpg_pf matches ..24 positioned ^ ^ ^1 run function rpg:pope_fight/boss/blood_step
