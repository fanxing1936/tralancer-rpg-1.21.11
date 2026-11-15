# 一阶段每刻（as 领主）。原版近战归零：普攻改由对得上动作的「刺」。
execute if entity @s[tag=!rpg.lu1f.init] run function rpg:lucifer_fight/p1/init
execute unless score @s rpg_l2_id matches 1.. run function rpg:lucifer_fight/new_id
execute unless score @s rpg_l2_st matches 2 if score @s rpg_dm_cd matches ..29 run scoreboard players set @s rpg_dm_cd 30
execute if score @s rpg_l2_st matches 3 run return run function rpg:lucifer_fight/p1/skill
scoreboard players set @s rpg_l2_st 2
execute if score @s rpg_l2_mc matches 1.. run scoreboard players remove @s rpg_l2_mc 1
execute if score @s rpg_l2_mc matches ..0 if score @s rpg_dm_ult matches ..0 if entity @e[tag=rpg.unit.f,distance=..4] run function rpg:lucifer_fight/p1/jab/start
