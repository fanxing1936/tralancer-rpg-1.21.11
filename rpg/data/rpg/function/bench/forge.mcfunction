execute store result storage rpg:bench d.nk int 1 run clear @s *[minecraft:custom_data~{rpg_mat:"sin_shard"}] 0
execute store result score #a rpg_fg run clear @s *[minecraft:item_model="rpg:world/blueprint_epic"] 0
execute store result score #b rpg_fg run clear @s *[minecraft:item_model="rpg:world/blueprint_legend"] 0
execute store result storage rpg:bench d.nbp int 1 run scoreboard players operation #a rpg_fg += #b rpg_fg
function rpg:bench/forge_m with storage rpg:bench d
