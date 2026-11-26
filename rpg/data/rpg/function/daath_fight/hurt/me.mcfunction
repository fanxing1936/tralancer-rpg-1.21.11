# 影子打中挑战者（as 挑战者；#pc 百分比）：最大生命 ×#pc%，会死就不扣、判负
execute unless score @s rpg_dt_ph matches 3 run return 0
execute store result score #a rpg_dt run attribute @s minecraft:max_health get 10
scoreboard players operation #a rpg_dt *= #pc rpg_dt
execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_sw=1..}] run scoreboard players operation #a rpg_dt *= #12 rpg_dt
execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_sw=1..}] run scoreboard players operation #a rpg_dt /= #10 rpg_dt
execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_blade=1..}] run scoreboard players operation #a rpg_dt *= #13 rpg_dt
execute if entity @e[type=minecraft:vindicator,tag=rpg.dt.it,scores={rpg_dt_blade=1..}] run scoreboard players operation #a rpg_dt /= #10 rpg_dt
scoreboard players operation #a rpg_dt /= #100 rpg_dt
execute store result score #hp rpg_dt run data get entity @s Health 10
execute store result score #ab rpg_dt run data get entity @s AbsorptionAmount 10
scoreboard players operation #hp rpg_dt += #ab rpg_dt
execute if score #a rpg_dt >= #hp rpg_dt run return run function rpg:daath_fight/hurt/fail
execute store result storage rpg:daath t.d double 0.1 run scoreboard players get #a rpg_dt
function rpg:daath_fight/hurt/m with storage rpg:daath t
