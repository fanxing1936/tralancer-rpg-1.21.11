scoreboard players operation #m rpg_jq = @s rpg_jq_t
scoreboard players set #k rpg_jq 5
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 if score @s rpg_jq_t matches ..28 as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s run function rpg:jacques_boss/cross/pulse
execute if score @s rpg_jq_t matches ..30 run particle minecraft:end_rod ~ ~1.2 ~ 0.5 1 0.5 0.03 2
execute if score @s rpg_jq_t matches 10 run playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.4
execute if score @s rpg_jq_t matches 20 run playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.7
execute if score @s rpg_jq_t matches 30 as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s run function rpg:jacques_boss/cross/blast
execute if score @s rpg_jq_t matches 62.. run function rpg:jacques_boss/stagger/end
