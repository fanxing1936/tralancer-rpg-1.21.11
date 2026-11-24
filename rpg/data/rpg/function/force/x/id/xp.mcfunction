scoreboard players operation #d rpg_fo *= #20 rpg_fo
execute if score @s rpg_sef matches 5.. run scoreboard players operation #d rpg_fo *= #2 rpg_fo
scoreboard players operation @s rpg_fo_xa += #d rpg_fo
scoreboard players operation #q rpg_fo = @s rpg_fo_xa
scoreboard players operation #q rpg_fo /= #100 rpg_fo
scoreboard players operation @s rpg_ex_xp += #q rpg_fo
scoreboard players operation @s rpg_fo_xa %= #100 rpg_fo
