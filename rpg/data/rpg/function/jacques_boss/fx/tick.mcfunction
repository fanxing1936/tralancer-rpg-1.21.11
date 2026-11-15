# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_jq_life 1
execute if score @s rpg_jq_life matches ..0 run return run kill @s
execute if entity @s[tag=rpg.jqb.arrow] run return run function rpg:jacques_boss/fx/arrow
execute if entity @s[tag=rpg.jqb.fire] run function rpg:jacques_boss/fx/fire
execute if entity @s[tag=rpg.jqb.firering] run function rpg:jacques_boss/fx/firering
execute if score @s rpg_jq_kd matches 1.. run function rpg:jacques_boss/fx/kind
