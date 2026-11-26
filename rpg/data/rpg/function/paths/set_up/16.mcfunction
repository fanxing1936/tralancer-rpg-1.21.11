execute unless score @s rpg_ps_16 matches 2..4 run return run function rpg:paths/page/16
execute if score @s rpg_ps_16 matches 2 run return run function rpg:paths/page/16
execute if score @s rpg_ps_16 matches 4 run return run function rpg:paths/take {n:16,s:2}
execute if score @s rpg_ps_11 matches 2 unless score @s rpg_pa_ff matches 1 run return run function rpg:paths/take_free {n:16,s:2}
execute store result score #g rpg_pa run clear @s *[minecraft:custom_data~{rpg_mat:"wash_gem"}] 0
execute if score #g rpg_pa matches 0 run return run function rpg:paths/no_gem {n:16}
clear @s *[minecraft:custom_data~{rpg_mat:"wash_gem"}] 1
function rpg:paths/take {n:16,s:2}
