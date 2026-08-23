# 冷却递减，顺带把剩余量画到屏幕下方那条唯一的 actionbar 上。
scoreboard players remove @s rpg_pact_cd 1
scoreboard players set @s rpg_hud 5
scoreboard players set @s rpg_hud_t 3
scoreboard players operation @s rpg_hud_p = #pact_full rpg_hud
scoreboard players operation @s rpg_hud_p -= @s rpg_pact_cd
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #pact_full rpg_hud
