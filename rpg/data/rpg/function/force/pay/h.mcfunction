# 路径赐福（add_paths.py）
execute if score @s rpg_ps_12 matches 2 run scoreboard players operation #fc rpg_fo *= #9 rpg_pa
execute if score @s rpg_ps_12 matches 2 run scoreboard players operation #fc rpg_fo /= #10 rpg_pa
scoreboard players set #ok rpg_fo 0
execute unless score @s rpg_mana >= #fc rpg_fo run return run function rpg:force/fail/say {m:"圣力不够"}
scoreboard players operation @s rpg_mana -= #fc rpg_fo
# 生命力：神职者 −30%（美丽阶起 −60%），同化 50 起 +50%，弥赛亚不扣
execute if score @s rpg_ident matches 3 unless score @s rpg_sef matches 5.. run scoreboard players operation #vc rpg_fo *= #7 rpg_fo
execute if score @s rpg_ident matches 3 if score @s rpg_sef matches 5.. run scoreboard players operation #vc rpg_fo *= #4 rpg_fo
execute if score @s rpg_ident matches 3 run scoreboard players operation #vc rpg_fo /= #10 rpg_fo
execute if score @s rpg_assim matches 50.. run scoreboard players operation #vc rpg_fo *= #15 rpg_fo
execute if score @s rpg_assim matches 50.. run scoreboard players operation #vc rpg_fo /= #10 rpg_fo
execute if score @s rpg_messiah matches 1 run scoreboard players set #vc rpg_fo 0
scoreboard players operation @s rpg_fo_vf += #vc rpg_fo
scoreboard players operation #q rpg_fo = @s rpg_fo_vf
scoreboard players operation #q rpg_fo /= #10 rpg_fo
scoreboard players operation @s rpg_vital -= #q rpg_fo
scoreboard players operation @s rpg_fo_vf %= #10 rpg_fo
execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0
scoreboard players set #ok rpg_fo 1
