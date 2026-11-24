# 抽一次身份（万分比，onboard_spec.ODDS）
execute if score @s rpg_ident matches 1.. run return run function rpg:onboard/ident/done
execute store result score #r rpg_ob run random value 0..9999
execute if score #r rpg_ob matches 0..5499 run scoreboard players set @s rpg_ident 1
execute if score #r rpg_ob matches 5500..7499 run scoreboard players set @s rpg_ident 2
execute if score #r rpg_ob matches 7500..8999 run scoreboard players set @s rpg_ident 3
execute if score #r rpg_ob matches 9000..9899 run scoreboard players set @s rpg_ident 4
execute if score #r rpg_ob matches 9900..9999 run function rpg:onboard/ident/unique
execute if score @s rpg_ident matches 4 store result score @s rpg_ident_sin run random value 1..7
execute if score @s rpg_ident matches 5..7 run scoreboard players set @s rpg_messiah 1
function rpg:onboard/ident/done
