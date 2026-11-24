# 影步（as/at 施放者）
scoreboard players operation #lv rpg_fo = @s rpg_k21
execute unless score #lv rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"还没学会影步"}
execute if score @s rpg_kc21 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc21
execute if score @s rpg_kc21 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc21 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc21 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc21 > #now rpg_fo run return run function rpg:force/cd_say
execute if score #lv rpg_fo matches 1 run scoreboard players set #fc rpg_fo 15
execute if score #lv rpg_fo matches 2 run scoreboard players set #fc rpg_fo 15
execute if score #lv rpg_fo matches 3 run scoreboard players set #fc rpg_fo 15
execute if score #lv rpg_fo matches 1 run scoreboard players set #xc rpg_fo 2
execute if score #lv rpg_fo matches 2 run scoreboard players set #xc rpg_fo 2
execute if score #lv rpg_fo matches 3 run scoreboard players set #xc rpg_fo 2
function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
execute if score #lv rpg_fo matches 1 run scoreboard players set #c rpg_fo 160
execute if score #lv rpg_fo matches 2 run scoreboard players set #c rpg_fo 140
execute if score #lv rpg_fo matches 3 run scoreboard players set #c rpg_fo 120
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc21 = #now rpg_fo
scoreboard players operation @s rpg_kc21 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/21/do
tag @s remove rpg.fo.me
