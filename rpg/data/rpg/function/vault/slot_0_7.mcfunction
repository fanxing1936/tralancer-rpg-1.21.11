tag @s remove rpg.vt.new
scoreboard players operation @s rpg_vt_id = #id rpg_vt
scoreboard players set @s rpg_vt_k 7
rotate @s ~315 0
loot replace entity @s contents loot rpg:vault/decoy
