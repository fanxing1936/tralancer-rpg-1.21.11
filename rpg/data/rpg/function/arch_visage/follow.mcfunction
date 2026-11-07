execute on passengers if entity @s[tag=rpg.av.part] run rotate @s ~ 0
execute unless score @s rpg_av_run matches 1 run return 0
execute if score @s rpg_av_anim matches 0 run return run function rpg:arch_visage/anim/idle/tick
execute if score @s rpg_av_anim matches 1 run return run function rpg:arch_visage/anim/walk/tick
execute if score @s rpg_av_anim matches 2 run return run function rpg:arch_visage/anim/spawn_attack/tick
