execute if score @s rpg_mk_t matches 2..12 run tp @s ~ ~0.55 ~
execute if score @s rpg_mk_t matches 2..28 run execute if score #w rpg_mk_i2 matches 1.. as @e[tag=rpg.mkb.diveto,distance=0..] at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run tp @s ~ ~ ~
execute if score @s rpg_mk_t matches 2..28 run execute if score #w rpg_mk_i2 matches ..0 as @e[tag=rpg.mkb.diveto,distance=0..] at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run tp @s ~ ~ ~
execute if score @s rpg_mk_t matches 2..28 run execute as @e[tag=rpg.mkb.divering,distance=0..] at @e[tag=rpg.mkb.diveto,limit=1,distance=0..] run tp @s ~ ~0.06 ~
execute if score @s rpg_mk_t matches 28 run playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 1 1.6
execute if score @s rpg_mk_t matches 34 run execute at @e[tag=rpg.mkb.diveto,limit=1,distance=0..] run tp @s ~ ~ ~
execute if score @s rpg_mk_t matches 34 run data merge entity @s {NoGravity:0b}
execute if score @s rpg_mk_t matches 34 run function rpg:michael/anim/enter/land
execute if score @s rpg_mk_t matches 35 run function rpg:michael_boss_i2/dive/hit
execute if score @s rpg_mk_t matches 58.. run function rpg:michael_boss_i2/sk/end
