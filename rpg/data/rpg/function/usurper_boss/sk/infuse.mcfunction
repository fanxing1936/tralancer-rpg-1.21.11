execute if score @s rpg_ub_t matches 120.. run return run function rpg:usurper_boss/infuse/end
execute unless entity @e[tag=rpg.usb.infused] run return run function rpg:usurper_boss/infuse/broken
scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 2
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 as @e[tag=rpg.usb.infused,limit=1] positioned ~ ~1.5 ~ facing entity @s eyes run function rpg:usurper_boss/infuse/beam
scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 6
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 at @e[tag=rpg.usb.infused,limit=1] run function rpg:usurper_boss/infuse/spark
execute if score @s rpg_ub_t matches 20 run playsound rpg:usurper.beam_loop hostile @a[distance=..32] ~ ~ ~ 0.8 1
execute if score @s rpg_ub_t matches 60 run playsound rpg:usurper.beam_loop hostile @a[distance=..32] ~ ~ ~ 0.8 1
