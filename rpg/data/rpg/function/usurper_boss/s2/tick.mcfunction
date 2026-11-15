scoreboard players operation #m rpg_ub = #tick rpg_ub
scoreboard players set #k rpg_ub 2
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 as @e[tag=rpg.usb.guard,distance=..80] at @s run function rpg:usurper_boss/auth/line
execute if score #m rpg_ub matches 0 as @e[tag=rpg.usb.abeam] run function rpg:usurper_boss/auth/check
execute if entity @s[tag=rpg.usb.guarded] unless entity @e[tag=rpg.usb.guard,distance=..120] run function rpg:usurper_boss/auth/fall
execute if entity @s[tag=rpg.usb.exposed] run function rpg:usurper_boss/weak/tick
scoreboard players operation #m rpg_ub = #tick rpg_ub
scoreboard players set #k rpg_ub 160
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 if score @s rpg_ub_busy matches ..0 run playsound minecraft:entity.evoker.ambient hostile @a[distance=..32] ~ ~ ~ 1 0.7
