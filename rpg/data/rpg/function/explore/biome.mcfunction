scoreboard players set #b rpg_xb 0
execute if biome ~ ~ ~ #rpg:ex/plains run scoreboard players set #b rpg_xb 1
execute if biome ~ ~ ~ #rpg:ex/forest run scoreboard players set #b rpg_xb 2
execute if biome ~ ~ ~ #rpg:ex/wildfield run scoreboard players set #b rpg_xb 3
execute if biome ~ ~ ~ #rpg:ex/lavender run scoreboard players set #b rpg_xb 4
execute if biome ~ ~ ~ #rpg:ex/golden run scoreboard players set #b rpg_xb 5
execute if biome ~ ~ ~ #rpg:ex/desert run scoreboard players set #b rpg_xb 6
execute if biome ~ ~ ~ #rpg:ex/snowfield run scoreboard players set #b rpg_xb 7
execute if biome ~ ~ ~ #rpg:ex/taiga run scoreboard players set #b rpg_xb 8
execute if biome ~ ~ ~ #rpg:ex/mesa run scoreboard players set #b rpg_xb 9
execute if biome ~ ~ ~ #rpg:ex/eroded run scoreboard players set #b rpg_xb 10
execute if biome ~ ~ ~ #rpg:ex/ashwood run scoreboard players set #b rpg_xb 11
execute if biome ~ ~ ~ #rpg:ex/stone run scoreboard players set #b rpg_xb 12
execute if biome ~ ~ ~ #rpg:ex/warped run scoreboard players set #b rpg_xb 13
execute if biome ~ ~ ~ #rpg:ex/glacier run scoreboard players set #b rpg_xb 14
execute if biome ~ ~ ~ #rpg:ex/alpine run scoreboard players set #b rpg_xb 15
execute if biome ~ ~ ~ #rpg:ex/volcano run scoreboard players set #b rpg_xb 16
execute if biome ~ ~ ~ #rpg:ex/war run scoreboard players set #b rpg_xb 17
execute if biome ~ ~ ~ #rpg:ex/cliffs run scoreboard players set #b rpg_xb 18
execute if biome ~ ~ ~ #rpg:ex/sea run scoreboard players set #b rpg_xb 19
execute if score #b rpg_xb = @s rpg_xb run return 0
scoreboard players operation @s rpg_xb = #b rpg_xb
execute if score #b rpg_xb matches 0 run return 0
execute if score #b rpg_xb matches 1 run return run function rpg:explore/b/plains
execute if score #b rpg_xb matches 2 run return run function rpg:explore/b/forest
execute if score #b rpg_xb matches 3 run return run function rpg:explore/b/wildfield
execute if score #b rpg_xb matches 4 run return run function rpg:explore/b/lavender
execute if score #b rpg_xb matches 5 run return run function rpg:explore/b/golden
execute if score #b rpg_xb matches 6 run return run function rpg:explore/b/desert
execute if score #b rpg_xb matches 7 run return run function rpg:explore/b/snowfield
execute if score #b rpg_xb matches 8 run return run function rpg:explore/b/taiga
execute if score #b rpg_xb matches 9 run return run function rpg:explore/b/mesa
execute if score #b rpg_xb matches 10 run return run function rpg:explore/b/eroded
execute if score #b rpg_xb matches 11 run return run function rpg:explore/b/ashwood
execute if score #b rpg_xb matches 12 run return run function rpg:explore/b/stone
execute if score #b rpg_xb matches 13 run return run function rpg:explore/b/warped
execute if score #b rpg_xb matches 14 run return run function rpg:explore/b/glacier
execute if score #b rpg_xb matches 15 run return run function rpg:explore/b/alpine
execute if score #b rpg_xb matches 16 run return run function rpg:explore/b/volcano
execute if score #b rpg_xb matches 17 run return run function rpg:explore/b/war
execute if score #b rpg_xb matches 18 run return run function rpg:explore/b/cliffs
execute if score #b rpg_xb matches 19 run return run function rpg:explore/b/sea
