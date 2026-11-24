execute store result storage rpg:alc d.a0 int 1 run clear @s *[minecraft:custom_data~{rite_tag:1b},!minecraft:custom_data~{rpg_strong_water:1b}] 0
execute store result storage rpg:alc d.a1 int 1 run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_bronze"}] 0
data modify storage rpg:alc d.z set value 0
function rpg:alc/show_21_m with storage rpg:alc d
