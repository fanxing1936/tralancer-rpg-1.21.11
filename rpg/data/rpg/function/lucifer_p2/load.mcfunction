# 路西法·二阶段计分板。由 add_lucifer_p2_model.py 生成。
scoreboard objectives add rpg_lu2_anim dummy
scoreboard objectives add rpg_lu2_t dummy
scoreboard objectives add rpg_lu2_mv dummy
scoreboard objectives add rpg_lu2_mc dummy
scoreboard objectives add rpg_lu2_x dummy
scoreboard objectives add rpg_lu2_z dummy
scoreboard objectives add rpg_lu2 dummy
scoreboard objectives add rpg_lu2_mat dummy
scoreboard objectives add rpg_lu2_flower dummy
execute unless score #phase rpg_lu2_mat matches 0..199 run scoreboard players set #phase rpg_lu2_mat 0
