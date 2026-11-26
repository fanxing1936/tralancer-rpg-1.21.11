# 路径赐福（add_paths.py）
execute if score @s rpg_ps_13 matches 2 run scoreboard players operation #c rpg_fo *= #92 rpg_pa
execute if score @s rpg_ps_13 matches 2 run scoreboard players operation #c rpg_fo /= #100 rpg_pa
# 冷却修正（#c 刻）：边缘者放魔力技能 −10%（美丽阶起 −20%）
execute unless score #tree rpg_fo matches 2 run return 0
execute unless score @s rpg_ident matches 2 run return 0
execute unless score @s rpg_sef matches 5.. run scoreboard players operation #c rpg_fo *= #9 rpg_fo
execute if score @s rpg_sef matches 5.. run scoreboard players operation #c rpg_fo *= #8 rpg_fo
scoreboard players operation #c rpg_fo /= #10 rpg_fo
