# 冶炼对话框的三步：20..28 选类型，30..32 选档次，40 开炉。
execute if score #do rpg_fg matches 20..28 run scoreboard players operation @s rpg_fg_arg = #do rpg_fg
execute if score #do rpg_fg matches 20..28 run scoreboard players remove @s rpg_fg_arg 20
execute if score #do rpg_fg matches 20..28 run function rpg:forge/smelt/count
execute if score #do rpg_fg matches 20..28 run return run function rpg:forge/smelt/tiers with storage rpg:forge d
execute if score #do rpg_fg matches 30..32 run scoreboard players operation @s rpg_fg_arg2 = #do rpg_fg
execute if score #do rpg_fg matches 30..32 run scoreboard players remove @s rpg_fg_arg2 30
execute if score #do rpg_fg matches 30..32 run return run function rpg:forge/smelt/check
execute if score #do rpg_fg matches 40 run return run function rpg:forge/smelt/start
