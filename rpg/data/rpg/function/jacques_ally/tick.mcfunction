# 每刻：有友军或残留特效时才做事。
execute if entity @e[type=minecraft:iron_golem,tag=rpg.jqa,limit=1] run scoreboard players set #fxt rpg_al 40
execute unless score #fxt rpg_al matches 1.. run return 0
scoreboard players remove #fxt rpg_al 1
execute as @e[type=minecraft:iron_golem,tag=rpg.jqa] at @s run function rpg:jacques_ally/unit
execute as @e[tag=rpg.jqa.fx] at @s run function rpg:jacques_ally/fx/tick
