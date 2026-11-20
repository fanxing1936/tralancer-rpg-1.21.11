# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_sl_life 1
execute if score @s rpg_sl_life matches ..0 run return run kill @s
execute if entity @s[tag=rpg.slb.cut] run return run function rpg:saul_boss/fx/cut
execute if entity @s[tag=rpg.slb.web] run function rpg:saul_boss/fx/web
execute if entity @s[tag=rpg.slb.rain] run return run function rpg:saul_boss/fx/rain
execute if entity @s[tag=rpg.slb.rainsword] run function rpg:saul_boss/fx/rainsword
execute if entity @s[tag=rpg.slb.bigsword] run function rpg:saul_boss/fx/bigsword
execute if score @s rpg_sl_kd matches 1.. run function rpg:saul_boss/fx/kind
