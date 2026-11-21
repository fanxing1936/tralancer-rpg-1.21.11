execute unless score @s rpg_fg_vid matches 1.. run scoreboard players add #vid rpg_fg 1
execute unless score @s rpg_fg_vid matches 1.. run scoreboard players operation @s rpg_fg_vid = #vid rpg_fg
scoreboard players operation #tv rpg_fg = @s rpg_fg_vid
execute as @a[tag=rpg.fg.atk,tag=rpg.fg.src.hatred] run function rpg:forge/src/hatred_atk
