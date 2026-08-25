
# @s 仍是召唤它的 Boss，执行位置是本次新侍从脚下。
scoreboard players operation @e[type=minecraft:vindicator,tag=rpg.pseudo_boom.minion_new,distance=..1,limit=1,sort=nearest] rpg_boom_id = @s rpg_boom_id
tag @e[type=minecraft:vindicator,tag=rpg.pseudo_boom.minion_new,distance=..1] remove rpg.pseudo_boom.minion_new
