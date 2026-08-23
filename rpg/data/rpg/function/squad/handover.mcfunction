# 把副手那件交给最近的自己人。
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..8,limit=1,sort=nearest] if score @s rpg_squad = #sq rpg_squad at @s run function rpg:squad/give_weapon
execute unless entity @e[type=minecraft:husk,tag=rpg.squad,distance=..8] run function rpg:squad/none_near
tag @s remove rpg.sq.boss
