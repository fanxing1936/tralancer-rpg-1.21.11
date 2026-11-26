# 出手（as/at 影子）：按形状判
execute if score @s rpg_dt_sh matches 1 run function rpg:daath_fight/shape/jab
execute if score @s rpg_dt_sh matches 2 run function rpg:daath_fight/shape/arc
execute if score @s rpg_dt_sh matches 3 run function rpg:daath_fight/shape/wide
execute if score @s rpg_dt_sh matches 4 run function rpg:daath_fight/shape/spin
execute if score @s rpg_dt_sh matches 5 run function rpg:daath_fight/shape/line
execute if score @s rpg_dt_sh matches 6 run function rpg:daath_fight/shape/smash
execute if entity @a[tag=rpg.dt.hit] run scoreboard players operation #pc rpg_dt = @s rpg_dt_pc
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
execute if score @s rpg_dt_blade matches 1.. run particle minecraft:smoke ^ ^1 ^1.6 0.6 0.4 0.6 0.02 10
