# 玩家在 #t 这座镇的声望 + $(n)（可以是负数：players add 不收负数，先放进 #rn）
$scoreboard players set #rn rpg_tl $(n)
execute if score #t rpg_tl matches 1 run scoreboard players operation @s rpg_rep_1 += #rn rpg_tl
execute if score #t rpg_tl matches 2 run scoreboard players operation @s rpg_rep_2 += #rn rpg_tl
execute if score #t rpg_tl matches 3 run scoreboard players operation @s rpg_rep_3 += #rn rpg_tl
execute if score #t rpg_tl matches 4 run scoreboard players operation @s rpg_rep_4 += #rn rpg_tl
execute if score #t rpg_tl matches 5 run scoreboard players operation @s rpg_rep_5 += #rn rpg_tl
execute if score #t rpg_tl matches 6 run scoreboard players operation @s rpg_rep_6 += #rn rpg_tl
execute if score #t rpg_tl matches 7 run scoreboard players operation @s rpg_rep_7 += #rn rpg_tl
execute if score #t rpg_tl matches 8 run scoreboard players operation @s rpg_rep_8 += #rn rpg_tl
execute if score #t rpg_tl matches 9 run scoreboard players operation @s rpg_rep_9 += #rn rpg_tl
execute if score #t rpg_tl matches 10 run scoreboard players operation @s rpg_rep_10 += #rn rpg_tl
execute if score #t rpg_tl matches 11 run scoreboard players operation @s rpg_rep_11 += #rn rpg_tl
execute if score #t rpg_tl matches 12 run scoreboard players operation @s rpg_rep_12 += #rn rpg_tl
execute if score #t rpg_tl matches 13 run scoreboard players operation @s rpg_rep_13 += #rn rpg_tl
execute if score #t rpg_tl matches 14 run scoreboard players operation @s rpg_rep_14 += #rn rpg_tl
execute if score #t rpg_tl matches 15 run scoreboard players operation @s rpg_rep_15 += #rn rpg_tl
execute if score #t rpg_tl matches 16 run scoreboard players operation @s rpg_rep_16 += #rn rpg_tl
execute if score #t rpg_tl matches 17 run scoreboard players operation @s rpg_rep_17 += #rn rpg_tl
execute if score #t rpg_tl matches 18 run scoreboard players operation @s rpg_rep_18 += #rn rpg_tl
execute if score #t rpg_tl matches 19 run scoreboard players operation @s rpg_rep_19 += #rn rpg_tl
execute if score #t rpg_tl matches 20 run scoreboard players operation @s rpg_rep_20 += #rn rpg_tl
function rpg:town/life/rep_get
function rpg:town/life/rep_tier
