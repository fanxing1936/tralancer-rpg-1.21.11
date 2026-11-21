particle minecraft:end_rod ~ ~0.3 ~ 3 0.05 3 0 2
execute if score @s rpg_fg_t matches 1.. run scoreboard players operation #t rpg_fg = @s rpg_fg_t
scoreboard players operation #t rpg_fg %= #20 rpg_fg
execute if score #t rpg_fg matches 0 run effect give @e[tag=rpg.unit,distance=..6] minecraft:strength 2 0 true
execute if score #t rpg_fg matches 0 run effect give @e[tag=rpg.unit,distance=..6] minecraft:resistance 2 0 true
execute if score #t rpg_fg matches 0 run effect give @a[distance=..6] minecraft:strength 2 0 true
execute if score #t rpg_fg matches 0 run effect give @a[distance=..6] minecraft:resistance 2 0 true
