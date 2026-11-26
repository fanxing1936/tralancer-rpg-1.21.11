execute store result score #l rpg_pa run experience query @s levels
scoreboard players operation #l rpg_pa /= #10 rpg_pa
execute if score #l rpg_pa matches 6.. run scoreboard players set #l rpg_pa 5
execute if score #l rpg_pa = @s rpg_pa_xl run return 0
scoreboard players operation @s rpg_pa_xl = #l rpg_pa
attribute @s minecraft:attack_damage modifier remove rpg:pa_11x
execute store result storage rpg:paths x.v float 0.01 run scoreboard players get #l rpg_pa
function rpg:paths/xl_m with storage rpg:paths x
