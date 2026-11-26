scoreboard players operation #m rpg_dt = @s rpg_dt_t
scoreboard players set #k rpg_dt 5
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute if score #m rpg_dt matches 0 run playsound minecraft:entity.generic.drink hostile @a[distance=..24] ~ ~ ~ 0.8 0.8
execute if score @s rpg_dt_t matches 1..30 run particle minecraft:witch ~ ~1.6 ~ 0.15 0.2 0.15 0 1
execute if score @s rpg_dt_t matches 34 run function rpg:daath_fight/drink/heal
execute if score @s rpg_dt_t matches 40.. run function rpg:daath_fight/sk/end
