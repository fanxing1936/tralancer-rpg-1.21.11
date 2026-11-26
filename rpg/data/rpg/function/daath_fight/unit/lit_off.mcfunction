tag @s remove rpg.dt.lit
execute if score @s rpg_dt_st matches 1 run function rpg:daath/look/dark
playsound minecraft:block.candle.extinguish hostile @a[distance=..48] ~ ~ ~ 0.8 0.6
