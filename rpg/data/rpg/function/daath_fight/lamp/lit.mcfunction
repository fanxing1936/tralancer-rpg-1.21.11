scoreboard players set @s rpg_dt_lt 160
scoreboard players set @s rpg_dt_pcd 560
playsound minecraft:block.beacon.activate block @a[distance=..40] ~ ~3 ~ 0.8 1.6
playsound minecraft:item.firecharge.use block @a[distance=..40] ~ ~3 ~ 0.6 1.4
particle minecraft:end_rod ~ ~3.6 ~ 0.3 0.4 0.3 0.05 20
setblock ~ ~5 ~ minecraft:light[level=15]
execute if entity @s[tag=rpg.dt.l0] positioned ~0.00 ~ ~6.00 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l1] positioned ~-2.77 ~ ~4.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l2] positioned ~-5.69 ~ ~1.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l3] positioned ~-5.69 ~ ~-1.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l4] positioned ~-2.77 ~ ~-4.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l5] positioned ~0.00 ~ ~-6.00 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l6] positioned ~2.77 ~ ~-4.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l7] positioned ~5.69 ~ ~-1.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l8] positioned ~5.69 ~ ~1.67 run function rpg:daath_fight/lamp/lit_at
execute if entity @s[tag=rpg.dt.l9] positioned ~2.77 ~ ~4.67 run function rpg:daath_fight/lamp/lit_at
