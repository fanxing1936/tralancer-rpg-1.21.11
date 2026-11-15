# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_ub_life 1
execute if score @s rpg_ub_life matches ..0 run return run kill @s
execute if entity @s[tag=rpg.usb.bolt] run return run function rpg:usurper_boss/fx/bolt
execute if score @s rpg_ub_kd matches 1.. run function rpg:usurper_boss/fx/kind
