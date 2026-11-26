# 堕天（as/at 施放者，#tree 是放它的那棵树）
execute unless score @s rpg_k26 matches 1.. run return run function rpg:force/fail/say {m:"终式要到王冠阶（第 10 阶）"}
execute if score @s rpg_kc26 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc26
execute if score @s rpg_kc26 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc26 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc26 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc26 > #now rpg_fo run return run function rpg:force/cd_say
scoreboard players set #fc rpg_fo 50
scoreboard players set #xc rpg_fo 0
execute if score @s rpg_ident matches 4 run scoreboard players set #xc rpg_fo 8
function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
scoreboard players set #c rpg_fo 3600
function rpg:force/pay/cd
execute if score @s rpg_ps_12 matches 3 run scoreboard players operation #c rpg_fo *= #8 rpg_pa
execute if score @s rpg_ps_12 matches 3 run scoreboard players operation #c rpg_fo /= #10 rpg_pa
scoreboard players operation @s rpg_kc26 = #now rpg_fo
scoreboard players operation @s rpg_kc26 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/26/do
tag @s remove rpg.fo.me
