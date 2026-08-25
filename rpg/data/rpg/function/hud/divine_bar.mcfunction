scoreboard players set @s rpg_hud_on 1
scoreboard players operation @s rpg_hud_p = @s rpg_lt_div_max
scoreboard players operation @s rpg_hud_p -= @s rpg_lt_div_cd
scoreboard players operation @s rpg_hud_p *= #hud_mini rpg_hud
scoreboard players operation @s rpg_hud_p /= @s rpg_lt_div_max
execute if score @s rpg_lt_divine matches 1 run return run function rpg:hud/divine_old
execute if score @s rpg_lt_div_max matches 300 run return run function rpg:hud/divine_borrow
execute if score @s rpg_lt_div_max matches 600 run return run function rpg:hud/divine_field
function rpg:hud/divine_beam
