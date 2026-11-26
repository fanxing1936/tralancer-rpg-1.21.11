scoreboard players set @s rpg_dt_sk 8
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b}
playsound rpg:daath.flash2 hostile @a[distance=..32] ~ ~ ~ 0.7 1.2
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute store result score @s rpg_dt_i run random value 0..2
execute if score @s rpg_dt_i matches 0 run function rpg:daath/anim/enter/roll_l
execute if score @s rpg_dt_i matches 1 run function rpg:daath/anim/enter/roll_r
execute if score @s rpg_dt_i matches 2 run function rpg:daath/anim/enter/roll_f
playsound minecraft:entity.player.attack.nodamage hostile @a[distance=..48] ~ ~ ~ 0.8 1
