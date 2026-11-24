# 地上的法阵（as/at 标记，每刻）
execute if score @s rpg_fo_k matches 36 if score @s rpg_fo_end <= #now rpg_fo run function rpg:force/x/zone/star_boom
execute if score @s rpg_fo_end <= #now rpg_fo run return run kill @s
scoreboard players operation #zt rpg_fo = @s rpg_fo_end
scoreboard players operation #zt rpg_fo -= #now rpg_fo
scoreboard players operation #zt rpg_fo %= #10 rpg_fo
scoreboard players operation #lv rpg_fo = @s rpg_fo_lv
execute if score @s rpg_fo_k matches 6 run function rpg:force/zone/sanct
execute if score @s rpg_fo_k matches 16 run function rpg:force/zone/abyss
execute if score @s rpg_fo_k matches 63 run function rpg:force/x/zone/pit
execute if score @s rpg_fo_k matches 36 run function rpg:force/x/zone/star
