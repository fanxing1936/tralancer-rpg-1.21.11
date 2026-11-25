scoreboard players set @s rpg_bgm_s 0
scoreboard players remove @s rpg_bgm_t 1
execute if score @s rpg_bgm_t matches ..0 run function rpg:bgm/next
