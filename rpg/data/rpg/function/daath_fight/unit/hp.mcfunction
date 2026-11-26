# 读血与折算（十分之一点）
scoreboard players operation #m rpg_dt = @s rpg_dt_orb
scoreboard players set #k rpg_dt 2
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute unless score #m rpg_dt matches 0 run return 0
execute store result score #h rpg_dt run data get entity @s Health 10
scoreboard players set #d rpg_dt 10240
scoreboard players operation #d rpg_dt -= #h rpg_dt
execute unless score #d rpg_dt matches 1.. run return run function rpg:daath_fight/bar/set
function rpg:daath_fight/unit/top
function rpg:daath_fight/unit/struck
function rpg:daath_fight/bar/set
