execute if score @s rpg_sl_t matches 1..39 run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_sl_t matches 1..39 as @e[tag=rpg.slb.aim,distance=..2] positioned as @s rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] run tp @s ~ ~ ~ ~ ~
execute if score @s rpg_sl_t matches 1..40 run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ^ ^1.4 ^1.2 0.05 0.05 0.05 0 2
execute if score @s rpg_sl_t matches 30 run playsound minecraft:item.trident.riptide_3 hostile @a[distance=..40] ~ ~ ~ 1 0.8
execute if score @s rpg_sl_t matches 40 run function rpg:saul/anim/enter/roll_f
execute if score @s rpg_sl_t matches 40..48 run function rpg:saul_boss/last/step
execute if score @s rpg_sl_t matches 49 run function rpg:saul/anim/enter/final
execute if score @s rpg_sl_t matches 50 run function rpg:saul_boss/last/strike
execute if score @s rpg_sl_t matches 133.. run function rpg:saul_boss/sk/end
