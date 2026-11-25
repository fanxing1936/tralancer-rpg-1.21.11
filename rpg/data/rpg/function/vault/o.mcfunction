execute if score @s rpg_vt_t matches 3 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6] run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.440f,0.440f,0.440f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s rpg_vt_t matches ..30 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6] at @s run rotate @s ~6 ~
execute if score @s rpg_vt_t matches 31.. as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=..8}] at @s run rotate @s ~1.5 ~
execute if score @s rpg_vt_t matches 31..124 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=9}] at @s run rotate @s ~1.5 ~
execute if score @s rpg_vt_t matches ..120 run particle minecraft:dust{color:[0.35,0.75,0.80],scale:0.7} ~ ~-0.45 ~ 1.1 0.05 1.1 0 4
execute if score @s rpg_vt_t matches 34 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=0}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 43 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=1}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 52 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=2}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 61 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=3}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 70 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=4}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 79 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=5}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 88 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=6}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 97 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=7}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 106 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=8}] at @s run function rpg:vault/one
execute if score @s rpg_vt_t matches 114 run playsound minecraft:block.trial_spawner.about_to_spawn_item block @a[distance=..20] ~ ~ ~ 1 0.6
execute if score @s rpg_vt_t matches 124 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=9}] run function rpg:vault/last
execute if score @s rpg_vt_t matches 125 run function rpg:vault/last_show
execute if score @s rpg_vt_t matches 134..175 as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=9}] at @s run rotate @s ~5 ~
execute if score @s rpg_vt_t matches 176.. run function rpg:vault/finish
