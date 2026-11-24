# 冶炼对话框的三步：20..28 选类型，30..32 选档次，40 开炉。50..59 罪器锻造、60..69 材料转换（add_forge_world.py）。
execute if score #do rpg_fg matches 200..259 run return run function rpg:alc/do
execute if score #do rpg_fg matches 50..59 run return run function rpg:forge/sin/do
execute if score #do rpg_fg matches 60..69 run return run function rpg:forge/conv/do
execute if score #do rpg_fg matches 70..79 run return run function rpg:forge/bp/do
execute if score #do rpg_fg matches 80..109 run return run function rpg:forge/bp/frag_do
execute if score #do rpg_fg matches 20..28 run scoreboard players operation @s rpg_fg_arg = #do rpg_fg
execute if score #do rpg_fg matches 20..28 run scoreboard players remove @s rpg_fg_arg 20
execute if score #do rpg_fg matches 20..28 run function rpg:forge/smelt/count
execute if score #do rpg_fg matches 20..28 run return run function rpg:forge/smelt/tiers with storage rpg:forge d
execute if score #do rpg_fg matches 30..32 run scoreboard players operation @s rpg_fg_arg2 = #do rpg_fg
execute if score #do rpg_fg matches 30..32 run scoreboard players remove @s rpg_fg_arg2 30
execute if score #do rpg_fg matches 30..32 run return run function rpg:forge/smelt/check
execute if score #do rpg_fg matches 40 run return run function rpg:forge/smelt/start
