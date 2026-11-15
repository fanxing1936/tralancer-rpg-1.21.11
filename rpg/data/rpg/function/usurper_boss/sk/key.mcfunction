scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 10
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score @s rpg_ub_t matches ..80 if score #m rpg_ub matches 0 run particle dust{color:[0.72,0.52,0.84],scale:1.5} ~ ~0.3 ~ 7 0.1 7 0 40 force
execute if score @s rpg_ub_t matches ..70 if score #m rpg_ub matches 5 run function rpg:usurper_boss/key/mote
execute if score @s rpg_ub_t matches 60 run execute as @e[tag=rpg.usb.keyhex] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{scale:[30f,1f,30f]}}
execute if score @s rpg_ub_t matches 80 run function rpg:usurper_boss/key/burst
execute if score @s rpg_ub_t matches 81..140 if score #m rpg_ub matches 0 run function rpg:usurper_boss/stagger_star
execute if score @s rpg_ub_t matches 140 run function rpg:usurper_boss/key/rise
execute if score @s rpg_ub_t matches 141.. run function rpg:usurper_boss/sk/end
