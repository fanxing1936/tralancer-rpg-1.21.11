# 献祭（as/at 施放者）
scoreboard players operation #lv rpg_fo = @s rpg_k19
execute unless score #lv rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"还没学会献祭"}
execute if score @s rpg_kc19 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc19
execute if score @s rpg_kc19 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc19 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc19 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc19 > #now rpg_fo run return run function rpg:force/cd_say
execute if score #lv rpg_fo matches 1 run scoreboard players set #fc rpg_fo 0
execute if score #lv rpg_fo matches 2 run scoreboard players set #fc rpg_fo 0
execute if score #lv rpg_fo matches 3 run scoreboard players set #fc rpg_fo 0
execute store result score #h rpg_fo run data get entity @s Health
execute unless score #h rpg_fo matches 8.. run return run function rpg:force/fail/say {m:"生命不够献祭"}
execute if score #lv rpg_fo matches 1 run scoreboard players set #xc rpg_fo 2
execute if score #lv rpg_fo matches 2 run scoreboard players set #xc rpg_fo 2
execute if score #lv rpg_fo matches 3 run scoreboard players set #xc rpg_fo 2
function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
execute if score #lv rpg_fo matches 1 run scoreboard players set #c rpg_fo 600
execute if score #lv rpg_fo matches 2 run scoreboard players set #c rpg_fo 520
execute if score #lv rpg_fo matches 3 run scoreboard players set #c rpg_fo 440
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc19 = #now rpg_fo
scoreboard players operation @s rpg_kc19 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/19/do
tag @s remove rpg.fo.me
