# 借柱（as/at 施放者）
scoreboard players operation #lv rpg_fo = @s rpg_k24
execute unless score #lv rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"还没学会借柱"}
execute if score @s rpg_kc24 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc24
execute if score @s rpg_kc24 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc24 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc24 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc24 > #now rpg_fo run return run function rpg:force/cd_say
execute if score #lv rpg_fo matches 1 run scoreboard players set #fc rpg_fo 40
execute if score #lv rpg_fo matches 2 run scoreboard players set #fc rpg_fo 35
execute if score #lv rpg_fo matches 3 run scoreboard players set #fc rpg_fo 30
execute unless entity @s[tag=rpg.pact] run return run function rpg:force/fail/say {m:"你没有契约可借"}
execute if score #lv rpg_fo matches 1 run scoreboard players set #xc rpg_fo 4
execute if score #lv rpg_fo matches 2 run scoreboard players set #xc rpg_fo 4
execute if score #lv rpg_fo matches 3 run scoreboard players set #xc rpg_fo 4
function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
execute if score #lv rpg_fo matches 1 run scoreboard players set #c rpg_fo 1800
execute if score #lv rpg_fo matches 2 run scoreboard players set #c rpg_fo 1500
execute if score #lv rpg_fo matches 3 run scoreboard players set #c rpg_fo 1200
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc24 = #now rpg_fo
scoreboard players operation @s rpg_kc24 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/24/do
tag @s remove rpg.fo.me
