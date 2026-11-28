execute if score @s rpg_mk_t matches 20 run function rpg:michael_boss_i2/sanctus/wave
execute if score @s rpg_mk_t matches 20 run scoreboard players set #wid rpg_mk_i2 1
execute if score @s rpg_mk_t matches 20 run execute as @e[tag=rpg.mkb.wavenew,distance=0..] run scoreboard players operation @s rpg_mk_r = #wid rpg_mk_i2
execute if score @s rpg_mk_t matches 20 run tag @e[tag=rpg.mkb.wavenew,distance=0..] remove rpg.mkb.wavenew
execute if score @s rpg_mk_t matches 18 run function rpg:michael/anim/enter/gong
execute if score @s rpg_mk_t matches 20 run playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.8
execute if score @s rpg_mk_t matches 50 run function rpg:michael_boss_i2/sanctus/wave
execute if score @s rpg_mk_t matches 50 run scoreboard players set #wid rpg_mk_i2 2
execute if score @s rpg_mk_t matches 50 run execute as @e[tag=rpg.mkb.wavenew,distance=0..] run scoreboard players operation @s rpg_mk_r = #wid rpg_mk_i2
execute if score @s rpg_mk_t matches 50 run tag @e[tag=rpg.mkb.wavenew,distance=0..] remove rpg.mkb.wavenew
execute if score @s rpg_mk_t matches 48 run function rpg:michael/anim/enter/gong
execute if score @s rpg_mk_t matches 50 run playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 0.9
execute if score @s rpg_mk_t matches 80 run function rpg:michael_boss_i2/sanctus/wave
execute if score @s rpg_mk_t matches 80 run scoreboard players set #wid rpg_mk_i2 3
execute if score @s rpg_mk_t matches 80 run execute as @e[tag=rpg.mkb.wavenew,distance=0..] run scoreboard players operation @s rpg_mk_r = #wid rpg_mk_i2
execute if score @s rpg_mk_t matches 80 run tag @e[tag=rpg.mkb.wavenew,distance=0..] remove rpg.mkb.wavenew
execute if score @s rpg_mk_t matches 78 run function rpg:michael/anim/enter/gong
execute if score @s rpg_mk_t matches 80 run playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 1.0
execute if score @s rpg_mk_t matches 88 run function rpg:michael_boss_i2/sanctus/wave
execute if score @s rpg_mk_t matches 88 run scoreboard players set #wid rpg_mk_i2 4
execute if score @s rpg_mk_t matches 88 run execute as @e[tag=rpg.mkb.wavenew,distance=0..] run scoreboard players operation @s rpg_mk_r = #wid rpg_mk_i2
execute if score @s rpg_mk_t matches 88 run tag @e[tag=rpg.mkb.wavenew,distance=0..] remove rpg.mkb.wavenew
execute if score @s rpg_mk_t matches 86 run function rpg:michael/anim/enter/gong
execute if score @s rpg_mk_t matches 88 run playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 1.4 1.2
execute if score @s rpg_mk_t matches 148 run function rpg:michael_boss_i2/sanctus/clear
execute if score @s rpg_mk_t matches 148 run function rpg:michael_boss_i2/solid/on
execute if score @s rpg_mk_t matches 148 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 148 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 188.. run function rpg:michael_boss_i2/sk/end
