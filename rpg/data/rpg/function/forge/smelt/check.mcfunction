execute if score @s rpg_fg_arg matches ..-1 run return 0
function rpg:forge/smelt/count
function rpg:forge/smelt/enough
scoreboard players set #ok rpg_fg 0
execute if score @s rpg_fg_arg2 matches 0 if score #ok0 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score @s rpg_fg_arg2 matches 1 if score #ok1 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score @s rpg_fg_arg2 matches 2 if score #ok2 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score #ok rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主材不够，这一档开不了炉","color":"#C04A3C","bold":false,"italic":false}]
execute if score #ns rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　至少需要 1 枚残魂","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players operation #souls rpg_fg = #ns rpg_fg
execute if score #souls rpg_fg matches 4.. run scoreboard players set #souls rpg_fg 3
execute store result storage rpg:forge d.souls int 1 run scoreboard players get #souls rpg_fg
execute if score @s rpg_fg_arg2 matches 0 run data modify storage rpg:forge d.mats set value "铁锭 ×6"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 0 run data modify storage rpg:forge d.what set value "长剑"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 1 run data modify storage rpg:forge d.what set value "战斧"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 2 run data modify storage rpg:forge d.what set value "重锤"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 3 run data modify storage rpg:forge d.what set value "长弓"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 4 run data modify storage rpg:forge d.what set value "劲弩"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 5 run data modify storage rpg:forge d.what set value "头盔"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 6 run data modify storage rpg:forge d.what set value "胸甲"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 7 run data modify storage rpg:forge d.what set value "护腿"
execute if score @s rpg_fg_arg2 matches 0 if score @s rpg_fg_arg matches 8 run data modify storage rpg:forge d.what set value "战靴"
execute if score @s rpg_fg_arg2 matches 1 run data modify storage rpg:forge d.mats set value "钻石 ×4"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 0 run data modify storage rpg:forge d.what set value "[勇者]长剑"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 1 run data modify storage rpg:forge d.what set value "[勇者]战斧"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 2 run data modify storage rpg:forge d.what set value "[勇者]重锤"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 3 run data modify storage rpg:forge d.what set value "[勇者]长弓"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 4 run data modify storage rpg:forge d.what set value "[勇者]劲弩"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 5 run data modify storage rpg:forge d.what set value "[勇者]头盔"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 6 run data modify storage rpg:forge d.what set value "[勇者]胸甲"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 7 run data modify storage rpg:forge d.what set value "[勇者]护腿"
execute if score @s rpg_fg_arg2 matches 1 if score @s rpg_fg_arg matches 8 run data modify storage rpg:forge d.what set value "[勇者]战靴"
execute if score @s rpg_fg_arg2 matches 2 run data modify storage rpg:forge d.mats set value "下界合金锭 ×1、钻石 ×4"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 0 run data modify storage rpg:forge d.what set value "[史诗]长剑"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 1 run data modify storage rpg:forge d.what set value "[史诗]战斧"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 2 run data modify storage rpg:forge d.what set value "[史诗]重锤"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 3 run data modify storage rpg:forge d.what set value "[史诗]长弓"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 4 run data modify storage rpg:forge d.what set value "[史诗]劲弩"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 5 run data modify storage rpg:forge d.what set value "[史诗]头盔"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 6 run data modify storage rpg:forge d.what set value "[史诗]胸甲"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 7 run data modify storage rpg:forge d.what set value "[史诗]护腿"
execute if score @s rpg_fg_arg2 matches 2 if score @s rpg_fg_arg matches 8 run data modify storage rpg:forge d.what set value "[史诗]战靴"
function rpg:forge/smelt/confirm with storage rpg:forge d
