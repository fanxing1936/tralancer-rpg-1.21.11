# 一支还没认过的箭。是不是我射的？`on origin` 会把 @s 换成射手。
scoreboard players set #mine rpg_mam 0
execute on origin if entity @s[tag=rpg.mam.shooter] run scoreboard players set #mine rpg_mam 1
# 只能由真正的射手把它标成已处理。多人时，甲的 watch 会先扫到乙的箭；
# 若先打 seen 再验 origin，乙轮到自己时就永远看不到这支箭了。
execute if score #mine rpg_mam matches 1 run tag @s add rpg.mam.seen
execute if score #mine rpg_mam matches 1 run function rpg:mammon/shot
