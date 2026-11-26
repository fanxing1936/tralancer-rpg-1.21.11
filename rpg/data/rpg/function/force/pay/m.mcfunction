# 路径赐福（add_paths.py）
execute if score @s rpg_ps_12 matches 2 run scoreboard players operation #fc rpg_fo *= #9 rpg_pa
execute if score @s rpg_ps_12 matches 2 run scoreboard players operation #fc rpg_fo /= #10 rpg_pa
execute if score @s rpg_ps_26 matches 3 run scoreboard players operation #fc rpg_fo *= #9 rpg_pa
execute if score @s rpg_ps_26 matches 3 run scoreboard players operation #fc rpg_fo /= #10 rpg_pa
scoreboard players set #ok rpg_fo 0
# 堕天期间：魔力技能不耗力、不涨魔化
execute if score @s rpg_fo_fl > #now rpg_fo run return run scoreboard players set #ok rpg_fo 1
execute if score @s rpg_force matches 2 unless score @s rpg_mana >= #fc rpg_fo run return run function rpg:force/fail/say {m:"魔力不够"}
execute if score @s rpg_force matches 3 unless score @s rpg_mana2 >= #fc rpg_fo run return run function rpg:force/fail/say {m:"魔力不够"}
execute if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana -= #fc rpg_fo
execute if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 -= #fc rpg_fo
scoreboard players operation @s rpg_taint += #xc rpg_fo
scoreboard players set #ok rpg_fo 1
