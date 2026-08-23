# 交给统一 HUD 渲染。反转要看的是"熬过去多少"，所以进度反着算：
# 图腾烧掉的那部分，才是受术者已经撑住的部分。
scoreboard players set @s rpg_hud 4
scoreboard players set @s rpg_hud_t 3
scoreboard players operation @s rpg_hud_p = #inv_full rpg_hud
scoreboard players operation @s rpg_hud_p -= #inv_now rpg_hud
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #inv_full rpg_hud
