# 选了第 #do - 80 张
execute store result score #c rpg_fg run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"bp_frag"}] 0
execute unless score #c rpg_fg matches 10.. run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　图纸碎片不够（要 10 片）","color":"#C04A3C","bold":false,"italic":false}]
execute if score #do rpg_fg matches 80 run loot give @s loot rpg:world/bp/starry
execute if score #do rpg_fg matches 81 run loot give @s loot rpg:world/bp/leviathan_song
execute if score #do rpg_fg matches 82 run loot give @s loot rpg:world/bp/flame_pride
execute if score #do rpg_fg matches 83 run loot give @s loot rpg:world/bp/wind_echo
execute if score #do rpg_fg matches 84 run loot give @s loot rpg:world/bp/mountain_roar
execute if score #do rpg_fg matches 85 run loot give @s loot rpg:world/bp/grave_bane
execute if score #do rpg_fg matches 86 run loot give @s loot rpg:world/bp/harp_crossbow
execute if score #do rpg_fg matches 87 run loot give @s loot rpg:world/bp/azure_seeker
execute if score #do rpg_fg matches 88 run loot give @s loot rpg:world/bp/gale_bow
execute if score #do rpg_fg matches 89 run loot give @s loot rpg:world/bp/jachin
execute if score #do rpg_fg matches 90 run loot give @s loot rpg:world/bp/boaz
execute if score #do rpg_fg matches 91 run loot give @s loot rpg:world/bp/molten_hammer
execute if score #do rpg_fg matches 92 run loot give @s loot rpg:world/bp/dark_sun
execute if score #do rpg_fg matches 93 run loot give @s loot rpg:world/bp/chainsaw
execute if score #do rpg_fg matches 94 run loot give @s loot rpg:world/bp/earth_spine
execute if score #do rpg_fg matches 95 run loot give @s loot rpg:world/bp/venom_fang
execute if score #do rpg_fg matches 96 run loot give @s loot rpg:world/bp/wind_bone
execute if score #do rpg_fg matches 97 run loot give @s loot rpg:world/bp/mischief_bow
execute if score #do rpg_fg matches 98 run loot give @s loot rpg:world/bp/vine_whip
execute if score #do rpg_fg matches 99 run loot give @s loot rpg:world/bp/truth_blade
execute if score #do rpg_fg matches 100 run loot give @s loot rpg:world/bp/crystal_roar
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"bp_frag"}] 10
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8
