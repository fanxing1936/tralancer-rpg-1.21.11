# 信条（as/at 施放者，#tree 是放它的那棵树）
execute unless score @s rpg_k31 matches 1.. run return run function rpg:force/fail/say {m:"还没习得「信条」"}
execute if score @s rpg_kc31 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc31
execute if score @s rpg_kc31 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc31 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc31 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc31 > #now rpg_fo run return run function rpg:force/cd_say
scoreboard players set #fc rpg_fo 30
scoreboard players set #vc rpg_fo 20
scoreboard players set #xc rpg_fo 2
scoreboard players set #ok rpg_fo 0
execute if score #tree rpg_fo matches 1 run function rpg:force/pay/h
execute if score #tree rpg_fo matches 2 run function rpg:force/pay/m
execute unless score #ok rpg_fo matches 1 run return 0
scoreboard players set #c rpg_fo 900
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc31 = #now rpg_fo
scoreboard players operation @s rpg_kc31 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/31/do
tag @s remove rpg.fo.me
