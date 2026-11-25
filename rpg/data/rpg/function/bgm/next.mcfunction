# 一首放完（或间歇结束）
execute if score @s rpg_bgm_c matches 10.. if score @s rpg_bgm_g matches 0 run return run function rpg:bgm/gap
scoreboard players set @s rpg_bgm_g 0
execute if score @s rpg_bgm_c matches 1 run return run function rpg:bgm/play/pl_gate
execute if score @s rpg_bgm_c matches 2 run return run function rpg:bgm/play/pl_hunt
execute if score @s rpg_bgm_c matches 3 run return run function rpg:bgm/play/pl_ash
execute if score @s rpg_bgm_c matches 4 run return run function rpg:bgm/play/pl_court
execute if score @s rpg_bgm_c matches 5 run return run function rpg:bgm/play/pl_moon
execute if score @s rpg_bgm_c matches 10 run return run function rpg:bgm/pick_10
execute if score @s rpg_bgm_c matches 11 run return run function rpg:bgm/pick_11
