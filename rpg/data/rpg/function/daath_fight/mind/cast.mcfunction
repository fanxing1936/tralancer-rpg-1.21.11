# 挑战者放了技能（#e 编号）：两秒半后还一记影版
scoreboard players operation #e rpg_dt = @a[tag=rpg.dt.me,limit=1] rpg_dt_cast
scoreboard players set @a[tag=rpg.dt.me,limit=1] rpg_dt_cast 0
execute if score #e rpg_dt = @s rpg_dt_eid run scoreboard players add @s rpg_dt_esm 1
execute unless score #e rpg_dt = @s rpg_dt_eid run scoreboard players set @s rpg_dt_esm 1
execute unless score #e rpg_dt = @s rpg_dt_eid run function rpg:daath_fight/mind/fresh
scoreboard players operation @s rpg_dt_eid = #e rpg_dt
execute if score @s rpg_dt_esm matches 3.. if entity @s[tag=!rpg.dt.loop] run function rpg:daath_fight/mind/loop
execute if score @s rpg_dt_ek matches 1.. run return 0
execute if score #e rpg_dt matches 1 run scoreboard players set @s rpg_dt_ek 1
execute if score #e rpg_dt matches 2 run scoreboard players set @s rpg_dt_ek 1
execute if score #e rpg_dt matches 13 run scoreboard players set @s rpg_dt_ek 1
execute if score #e rpg_dt matches 3 run scoreboard players set @s rpg_dt_ek 2
execute if score #e rpg_dt matches 11 run scoreboard players set @s rpg_dt_ek 2
execute if score #e rpg_dt matches 15 run scoreboard players set @s rpg_dt_ek 2
execute if score #e rpg_dt matches 22 run scoreboard players set @s rpg_dt_ek 2
execute if score #e rpg_dt matches 4 run scoreboard players set @s rpg_dt_ek 3
execute if score #e rpg_dt matches 14 run scoreboard players set @s rpg_dt_ek 3
execute if score #e rpg_dt matches 10 run scoreboard players set @s rpg_dt_ek 4
execute if score #e rpg_dt matches 16 run scoreboard players set @s rpg_dt_ek 4
execute if score #e rpg_dt matches 12 run scoreboard players set @s rpg_dt_ek 5
execute if score #e rpg_dt matches 21 run scoreboard players set @s rpg_dt_ek 5
execute if score #e rpg_dt matches 5 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 6 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 7 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 17 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 18 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 19 run scoreboard players set @s rpg_dt_ek 6
execute if score #e rpg_dt matches 8 run scoreboard players set @s rpg_dt_ek 7
execute if score #e rpg_dt matches 23 run scoreboard players set @s rpg_dt_ek 7
execute if score #e rpg_dt matches 24 run scoreboard players set @s rpg_dt_ek 7
execute if score #e rpg_dt matches 9 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 25 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 26 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 31 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 32 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 33 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 34 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 35 run scoreboard players set @s rpg_dt_ek 8
execute if score #e rpg_dt matches 36 run scoreboard players set @s rpg_dt_ek 8
execute if score @s rpg_dt_ek matches 1.. run scoreboard players set @s rpg_dt_et 50
execute if score @s rpg_dt_ek matches 1.. run function rpg:daath_fight/eye/skill
