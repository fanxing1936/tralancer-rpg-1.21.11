# 旧主动技现代化：using_item 每刻推进一格，满 30 刻只触发一次。
advancement revoke @s only rpg:item/ashes
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players set @s rpg_ashes_hold 3
execute if entity @s[tag=rpg.h.ashes_tag1,scores={rpg_ashes_chg=..29}] run scoreboard players add @s rpg_ashes_chg 1
execute at @s if entity @s[tag=rpg.h.ashes_tag1] run particle minecraft:dust_color_transition{from_color:[0.12,0.12,0.12],to_color:[0.45,0.1,0.02],scale:1.4} ~ ~1 ~ 0.35 0.5 0.35 0.03 8
execute at @s if entity @s[tag=rpg.h.ashes_tag1,scores={rpg_ashes_chg=1}] run playsound minecraft:item.mace.smash_air player @s ~ ~ ~ 0.7 0.7
execute at @s if entity @s[tag=rpg.h.ashes_tag1,scores={rpg_ashes_chg=15}] run playsound minecraft:item.mace.smash_air player @s ~ ~ ~ 0.8 1.1
execute at @s if entity @s[tag=rpg.h.ashes_tag1,scores={rpg_ashes_chg=25}] run playsound minecraft:item.mace.smash_air player @s ~ ~ ~ 0.9 1.5
execute if entity @s[tag=rpg.h.ashes_tag1,scores={rpg_ashes_chg=30}] run function rpg:item/legacy/ashes_cast
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players set @s rpg_hud 8
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players set @s rpg_hud_t 3
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players operation @s rpg_hud_p = @s rpg_ashes_chg
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
execute if entity @s[tag=rpg.h.ashes_tag1] run scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud
execute if entity @s[scores={rpg_hud_p=10..}] run scoreboard players set @s rpg_hud_p 10
