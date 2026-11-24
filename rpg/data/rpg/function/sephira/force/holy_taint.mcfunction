# 圣力者（as 玩家）：沾上的每一点魔化 → 1 点生命力损失 + 1 点同化；圣子、圣灵减半
scoreboard players operation #d rpg_sef = @s rpg_taint
scoreboard players set @s rpg_taint 0
execute if score @s rpg_messiah matches 1 run scoreboard players operation #d rpg_sef /= #2 rpg_sef
scoreboard players operation @s rpg_vital -= #d rpg_sef
scoreboard players operation @s rpg_assim += #d rpg_sef
# 握着圣器：每 30 秒扣 1 点生命力（弥赛亚不扣）
execute if entity @s[tag=rpg.holy] unless score @s rpg_messiah matches 1 run scoreboard players add @s rpg_fz_h 1
execute if score @s rpg_fz_h matches 15.. run scoreboard players remove @s rpg_vital 1
execute if score @s rpg_fz_h matches 15.. run scoreboard players set @s rpg_fz_h 0
# 不在契约里：同化每 10 分钟回落 1 点
execute if entity @s[tag=!rpg.pact] if score @s rpg_assim matches 1.. run scoreboard players add @s rpg_fz_t 1
execute if score @s rpg_fz_t matches 300.. run scoreboard players remove @s rpg_assim 1
execute if score @s rpg_fz_t matches 300.. run scoreboard players set @s rpg_fz_t 0
execute if score @s rpg_vital matches ..-1 run scoreboard players set @s rpg_vital 0
execute if score @s rpg_assim matches 100.. run function rpg:sephira/force/fall
