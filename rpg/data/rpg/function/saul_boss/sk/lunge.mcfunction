execute if score @s rpg_sl_t matches 1..14 run execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 1..14 as @e[tag=rpg.slb.lungewarn,distance=..2] positioned as @s rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] run tp @s ~ ~ ~ ~ ~
execute if score @s rpg_sl_t matches 16 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 16 run playsound rpg:saul.roll hostile @a[distance=..24] ~ ~ ~ 1 1
execute if score @s rpg_sl_t matches 16..24 run function rpg:saul_boss/lunge/step
execute if score @s rpg_sl_t matches 25 run function rpg:saul/anim/enter/thrust
execute if score @s rpg_sl_t matches 26 run function rpg:saul_boss/strike/lunge
execute if score @s rpg_sl_t matches 33.. run function rpg:saul_boss/sk/end
