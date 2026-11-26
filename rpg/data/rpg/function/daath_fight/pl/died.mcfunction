# 其他原因死了：等复活（躺着的时候给东西会丢），再把掉在场地里的东西送到脚下，判负
execute store result score #h rpg_dt run data get entity @s Health 10
execute if score #h rpg_dt matches ..0 run return run function rpg:daath_fight/pl/keep
scoreboard players set @s rpg_dt_dc 0
tag @s remove rpg.dt.kept
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
function rpg:daath_fight/pl/loot_m with storage rpg:daath t
scoreboard players add @s rpg_dt_n 1
tag @s add rpg.dt.dead
function rpg:daath_fight/pl/out
scoreboard players set @s rpg_dt_cd 2400
