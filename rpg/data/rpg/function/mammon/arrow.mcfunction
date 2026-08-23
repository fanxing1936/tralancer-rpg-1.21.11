# 一支还没认过的箭。是不是我射的？`on origin` 会把 @s 换成射手。
tag @s add rpg.mam.seen
scoreboard players set #mine rpg_mam 0
execute on origin if entity @s[tag=rpg.mam.shooter] run scoreboard players set #mine rpg_mam 1
execute if score #mine rpg_mam matches 1 run function rpg:mammon/shot
