# 屏幕下方状态行里的符石能量（rpg:hud/status 调用）。占第一个空槽。
scoreboard players operation #e rpg_fg = @s rpg_fg_en
scoreboard players operation #e rpg_fg /= #10 rpg_fg
execute if score #e rpg_fg matches 0 run data modify storage rpg:forge hud.v set value '{"text":"▱▱▱▱▱▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 1 run data modify storage rpg:forge hud.v set value '{"text":"▰▱▱▱▱▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 2 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▱▱▱▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 3 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▱▱▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 4 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▱▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 5 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▱▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 6 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▰▱▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 7 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▰▰▱▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 8 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▰▰▰▱▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 9 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▰▰▰▰▱","color":"#FFFFFF","italic":false}'
execute if score #e rpg_fg matches 10 run data modify storage rpg:forge hud.v set value '{"text":"▰▰▰▰▰▰▰▰▰▰","color":"#70DB70","italic":false}'
scoreboard players set @s rpg_hud_on 1
execute if data storage rpg:hud {d:'{"text":""}'} run return run function rpg:forge/hud_d
execute if data storage rpg:hud {c:'{"text":""}'} run return run function rpg:forge/hud_c
execute if data storage rpg:hud {b:'{"text":""}'} run return run function rpg:forge/hud_b
