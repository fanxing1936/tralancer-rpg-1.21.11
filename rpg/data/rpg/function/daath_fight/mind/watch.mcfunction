# 每刻记：远近、站着不动、刚放的技能、刚喝的药（as/at 影子）
execute if entity @a[tag=rpg.dt.me,distance=..8] run scoreboard players set @s rpg_dt_far 0
execute unless entity @a[tag=rpg.dt.me,distance=..8] run scoreboard players add @s rpg_dt_far 1
execute if score @s rpg_dt_melt matches 1.. run scoreboard players remove @s rpg_dt_melt 1
execute if score @s rpg_dt_melt matches 0 run scoreboard players set @s rpg_dt_mel 0
execute if score @s rpg_dt_scd matches 1.. run scoreboard players remove @s rpg_dt_scd 1
execute if score @s rpg_dt_gcd matches 1.. run scoreboard players remove @s rpg_dt_gcd 1
execute if score @s rpg_dt_et matches 1.. run scoreboard players remove @s rpg_dt_et 1
execute if score @a[tag=rpg.dt.me,limit=1] rpg_dt_cast matches 1.. run function rpg:daath_fight/mind/cast
execute if score @a[tag=rpg.dt.me,limit=1] rpg_dt_drk matches 1.. run function rpg:daath_fight/mind/drank
scoreboard players operation #m rpg_dt = @s rpg_dt_orb
scoreboard players set #k rpg_dt 10
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute if score #m rpg_dt matches 0 run function rpg:daath_fight/mind/still
