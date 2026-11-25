tag @s remove rpg.vt.new
scoreboard players operation @s rpg_vt_id = #id rpg_vt
scoreboard players set @s rpg_vt_k 8
rotate @s ~288 0
loot replace entity @s contents loot rpg:trial/ominous_key
