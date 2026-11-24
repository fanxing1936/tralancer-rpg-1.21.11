# 千刀（as/at 施放者，#tree 是放它的那棵树）
execute unless score @s rpg_k34 matches 1.. run return run function rpg:force/fail/say {m:"还没习得「千刀」"}
execute if score @s rpg_kc34 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc34
execute if score @s rpg_kc34 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc34 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc34 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc34 > #now rpg_fo run return run function rpg:force/cd_say
scoreboard players set #fc rpg_fo 30
scoreboard players set #vc rpg_fo 30
scoreboard players set #xc rpg_fo 3
scoreboard players set #ok rpg_fo 0
execute if score #tree rpg_fo matches 1 run function rpg:force/pay/h
execute if score #tree rpg_fo matches 2 run function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
scoreboard players set #c rpg_fo 400
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc34 = #now rpg_fo
scoreboard players operation @s rpg_kc34 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/34/do
tag @s remove rpg.fo.me
