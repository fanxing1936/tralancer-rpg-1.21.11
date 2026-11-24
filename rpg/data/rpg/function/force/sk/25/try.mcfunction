# 哈利路亚（as/at 施放者，#tree 是放它的那棵树）
execute unless score @s rpg_k25 matches 1.. run return run function rpg:force/fail/say {m:"终式要到王冠阶（第 10 阶）"}
execute if score @s rpg_kc25 > #now rpg_fo run scoreboard players operation #s rpg_fo = @s rpg_kc25
execute if score @s rpg_kc25 > #now rpg_fo run scoreboard players operation #s rpg_fo -= #now rpg_fo
execute if score @s rpg_kc25 > #now rpg_fo run scoreboard players add #s rpg_fo 19
execute if score @s rpg_kc25 > #now rpg_fo run scoreboard players operation #s rpg_fo /= #20 rpg_fo
execute if score @s rpg_kc25 > #now rpg_fo run return run function rpg:force/cd_say
tag @s add rpg.fo.self
scoreboard players set #ok rpg_fo 1
execute if score @s rpg_ident matches 6 unless entity @e[type=minecraft:player,tag=rpg.fo.down,tag=!rpg.fo.self] run scoreboard players set #ok rpg_fo 0
tag @s remove rpg.fo.self
execute unless score #ok rpg_fo matches 1 run return run function rpg:force/fail/say {m:"没有 60 秒内倒下的队友可以复活"}
scoreboard players set #fc rpg_fo 80
scoreboard players set #vc rpg_fo 60
function rpg:force/pay/h
execute unless score #ok rpg_fo matches 1 run return 0
scoreboard players set #c rpg_fo 3600
execute if score @s rpg_ident matches 6 run scoreboard players set #c rpg_fo 12000
function rpg:force/pay/cd
scoreboard players operation @s rpg_kc25 = #now rpg_fo
scoreboard players operation @s rpg_kc25 += #c rpg_fo
tag @s add rpg.fo.me
function rpg:force/sk/25/do
tag @s remove rpg.fo.me
