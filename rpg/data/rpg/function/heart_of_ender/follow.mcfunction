execute on passengers if entity @s[tag=rpg.he.part] run rotate @s ~ 0
execute unless score @s rpg_he_run matches 1 run return 0
execute if score @s rpg_he_anim matches 0 run return run function rpg:heart_of_ender/anim/idle/tick
execute if score @s rpg_he_anim matches 1 run return run function rpg:heart_of_ender/anim/walk/tick
execute if score @s rpg_he_anim matches 2 run return run function rpg:heart_of_ender/anim/mortar/tick
execute if score @s rpg_he_anim matches 3 run return run function rpg:heart_of_ender/anim/cross_beam/tick
execute if score @s rpg_he_anim matches 4 run return run function rpg:heart_of_ender/anim/sink/tick
execute if score @s rpg_he_anim matches 5 run return run function rpg:heart_of_ender/anim/rise/tick
execute if score @s rpg_he_anim matches 6 run return run function rpg:heart_of_ender/anim/death/tick
