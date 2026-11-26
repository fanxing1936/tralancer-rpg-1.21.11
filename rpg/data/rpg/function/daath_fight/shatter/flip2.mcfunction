# 第 3 批翻面
execute positioned ~0.00 ~ ~7.50 run function rpg:daath_fight/shatter/f1
execute positioned ~-0.00 ~ ~-7.50 run function rpg:daath_fight/shatter/f1
execute positioned ~6.51 ~ ~15.71 run function rpg:daath_fight/shatter/f2
execute positioned ~-15.71 ~ ~6.51 run function rpg:daath_fight/shatter/f2
execute positioned ~-17.00 ~ ~0.00 run function rpg:daath_fight/shatter/f2
execute positioned ~-0.00 ~ ~-17.00 run function rpg:daath_fight/shatter/f2
execute as @a[tag=rpg.dt.hit] at @s run effect give @s minecraft:levitation 1 4 true
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 12
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 0.7
playsound minecraft:entity.generic.splash hostile @a[distance=..48] ~ ~ ~ 0.8 0.5
