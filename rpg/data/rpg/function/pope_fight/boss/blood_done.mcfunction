# 祭品化为圣力。
kill @e[tag=rpg.pf.line]
execute as @e[type=minecraft:vindicator,tag=rpg.pf.sac] at @s run particle dust{color:[1.000f,0.949f,0.659f],scale:1.6} ~ ~1 ~ 0.5 1 0.5 0.1 24 normal
execute as @e[type=minecraft:vindicator,tag=rpg.pf.sac] run function rpg:tower_guard/ai/remove
execute store result score #hp rpg_pf run data get entity @s Health
scoreboard players add #hp rpg_pf 60
execute if score #hp rpg_pf matches 1001.. run scoreboard players set #hp rpg_pf 1000
execute store result entity @s Health float 1 run scoreboard players get #hp rpg_pf
playsound rpg:pope.haha hostile @a[distance=..32] ~ ~ ~ 1 1
function rpg:pope_fight/boss/end
