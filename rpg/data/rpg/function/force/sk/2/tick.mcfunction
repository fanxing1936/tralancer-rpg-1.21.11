# 断罪印（as/at 被标记的实体，每刻）：比上一刻少掉的血 × 加成，补一刀
execute if score @s rpg_fo_end <= #now rpg_fo run return run function rpg:force/sk/2/off
particle minecraft:wax_off ~ ~2.3 ~ 0.1 0.05 0.1 0 1
execute store result score #h rpg_fo run data get entity @s Health 10
execute if score #h rpg_fo >= @s rpg_fo_hp run return run scoreboard players operation @s rpg_fo_hp = #h rpg_fo
scoreboard players operation #dmg rpg_fo = @s rpg_fo_hp
scoreboard players operation #dmg rpg_fo -= #h rpg_fo
scoreboard players operation #dmg rpg_fo *= @s rpg_fo_mk
scoreboard players operation #dmg rpg_fo /= #100 rpg_fo
scoreboard players set #hm rpg_fo 10
execute if score #dmg rpg_fo matches 1.. run function rpg:force/hit
execute if score #dmg rpg_fo matches 1.. run particle minecraft:crit ~ ~1.2 ~ 0.3 0.4 0.3 0.2 8
execute store result score @s rpg_fo_hp run data get entity @s Health 10
