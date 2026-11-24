# 魔力不会自己回：每造成 2 点伤害 +1（击杀 +4 在 rpg:sephira/kill，魔化每涨 1 点 +3 在魔化结算里）
scoreboard players operation #q rpg_sef = @s rpg_fz_dd
scoreboard players operation #q rpg_sef /= #20 rpg_sef
execute if score @s rpg_force matches 2 run scoreboard players operation @s rpg_mana += #q rpg_sef
execute if score @s rpg_force matches 3 run scoreboard players operation @s rpg_mana2 += #q rpg_sef
