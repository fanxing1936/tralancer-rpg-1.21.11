# 旧主动技现代化：using_item 每刻推进一格，满 30 刻只触发一次。
advancement revoke @s only rpg:item/typhoon
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players set @s rpg_wind_hold 3
execute if entity @s[tag=rpg.h.typhoon_tag1,scores={rpg_wind_chg=..29}] run scoreboard players add @s rpg_wind_chg 1
execute at @s if entity @s[tag=rpg.h.typhoon_tag1] run particle minecraft:dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:1.4} ~ ~1 ~ 0.35 0.5 0.35 0.03 8
execute at @s if entity @s[tag=rpg.h.typhoon_tag1,scores={rpg_wind_chg=1}] run playsound minecraft:item.trident.return player @s ~ ~ ~ 0.7 0.7
execute at @s if entity @s[tag=rpg.h.typhoon_tag1,scores={rpg_wind_chg=15}] run playsound minecraft:item.trident.return player @s ~ ~ ~ 0.8 1.1
execute at @s if entity @s[tag=rpg.h.typhoon_tag1,scores={rpg_wind_chg=25}] run playsound minecraft:item.trident.return player @s ~ ~ ~ 0.9 1.5
execute if entity @s[tag=rpg.h.typhoon_tag1,scores={rpg_wind_chg=30}] run function rpg:item/legacy/typhoon_cast
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players set @s rpg_hud 7
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players set @s rpg_hud_t 3
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players operation @s rpg_hud_p = @s rpg_wind_chg
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
execute if entity @s[tag=rpg.h.typhoon_tag1] run scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud
execute if entity @s[scores={rpg_hud_p=10..}] run scoreboard players set @s rpg_hud_p 10
