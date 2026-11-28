execute if score @s rpg_mk_t matches 1..13 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_t matches 1..13 run execute as @e[tag=rpg.mkb.dashwarn,distance=..2] positioned as @s rotated as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..] run tp @s ~ ~ ~ ~ ~
execute if score @s rpg_mk_t matches 16 run function rpg:michael/anim/enter/roll_f
execute if score @s rpg_mk_t matches 16 run playsound minecraft:entity.phantom.flap hostile @a[distance=..32] ~ ~ ~ 1.6 0.8
execute if score @s rpg_mk_t matches 16..21 run function rpg:michael_boss_i3/dash/step
execute if score @s rpg_mk_t matches 22 run function rpg:michael_boss_i3/dash/hit
execute if score @s rpg_mk_t matches 38.. run function rpg:michael_boss_i3/sk/end
