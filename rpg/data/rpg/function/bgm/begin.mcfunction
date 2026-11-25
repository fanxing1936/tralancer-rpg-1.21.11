# 从头起：主世界先静一小会儿
scoreboard players operation @s rpg_bgm_c = @s rpg_bgm_w
scoreboard players set @s rpg_bgm_s 0
scoreboard players set @s rpg_bgm_g 0
execute if score @s rpg_bgm_c matches 10.. run return run function rpg:bgm/begin_ow
function rpg:bgm/next
