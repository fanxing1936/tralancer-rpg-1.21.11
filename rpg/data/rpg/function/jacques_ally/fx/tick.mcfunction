# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_al_life 1
execute if score @s rpg_al_life matches ..0 run return run kill @s
execute if score @s rpg_al_kd matches 1.. run function rpg:jacques_ally/fx/kind
