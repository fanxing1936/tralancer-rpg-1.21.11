# 圣光矛（as/at 施放者）
scoreboard players operation #lv rpg_fo = @s rpg_k01
execute unless score #lv rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"还没学会圣光矛"}
execute if score @s rpg_kc01 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc01
execute if score @s rpg_kc01 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc01 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc01 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc01 > #now rpg_fo run return run function rpg:force/cd_say
execute if score #lv rpg_fo matches 1 run scoreboard players set #fc rpg_fo 20
execute if score #lv rpg_fo matches 2 run scoreboard players set #fc rpg_fo 20
execute if score #lv rpg_fo matches 3 run scoreboard players set #fc rpg_fo 18
execute if score #lv rpg_fo matches 1 run scoreboard players set #vc rpg_fo 10
execute if score #lv rpg_fo matches 2 run scoreboard players set #vc rpg_fo 10
execute if score #lv rpg_fo matches 3 run scoreboard players set #vc rpg_fo 10
function rpg:force/pay/h
execute unless score #ok rpg_fo matches 1 run return 0
execute if score #lv rpg_fo matches 1 run scoreboard players set #c rpg_fo 100
execute if score #lv rpg_fo matches 2 run scoreboard players set #c rpg_fo 80
execute if score #lv rpg_fo matches 3 run scoreboard players set #c rpg_fo 60
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc01 = #now rpg_fo
scoreboard players operation @s rpg_kc01 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/1/do
tag @s remove rpg.fo.me
