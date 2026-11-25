tag @s remove rpg.vt.new
scoreboard players operation @s rpg_vt_id = #id rpg_vt
scoreboard players set @s rpg_vt_k 0
rotate @s ~0 0
scoreboard players operation #c rpg_vt = #id rpg_vt
function rpg:vault/roll
