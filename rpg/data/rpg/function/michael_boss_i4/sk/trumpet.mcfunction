execute if score @s rpg_mk_t matches 2..9 run tp @s ~ ~0.5 ~
execute if score @s rpg_mk_t matches 18 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 20 run playsound minecraft:item.goat_horn.sound.0 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 20 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 20 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 38 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 40 run playsound minecraft:item.goat_horn.sound.1 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 40 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 40 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 58 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 60 run playsound minecraft:item.goat_horn.sound.2 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 60 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 60 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 78 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 80 run playsound minecraft:item.goat_horn.sound.3 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 80 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 80 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 98 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 100 run playsound minecraft:item.goat_horn.sound.4 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 100 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 100 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 118 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 120 run playsound minecraft:item.goat_horn.sound.5 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 120 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 120 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/mark
execute if score @s rpg_mk_t matches 138 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 140 run playsound minecraft:item.goat_horn.sound.6 hostile @a[distance=..64] ~ ~ ~ 2 1
execute if score @s rpg_mk_t matches 140 run execute if score #w rpg_mk_i4 matches 1.. at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run function rpg:michael_boss_i4/trumpet/last
execute if score @s rpg_mk_t matches 140 run execute if score #w rpg_mk_i4 matches ..0 at @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] run function rpg:michael_boss_i4/trumpet/last
execute if score @s rpg_mk_t matches 170 run tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..]
execute if score @s rpg_mk_t matches 170 run data merge entity @s {NoGravity:0b}
execute if score @s rpg_mk_t matches 170 run tag @s remove rpg.mkb.air
execute if score @s rpg_mk_t matches 170 run function rpg:michael/anim/enter/land
execute if score @s rpg_mk_t matches 172 run function rpg:michael_boss_i4/solid/on
execute if score @s rpg_mk_t matches 172 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 172 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 212.. run function rpg:michael_boss_i4/sk/end
