scoreboard players set #need_s rpg_fg 8
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 2 run scoreboard players set #need_s rpg_fg 4
scoreboard players set #need_n rpg_fg 1
execute if score @s rpg_ident matches 2 run scoreboard players set #need_n rpg_fg 0
execute store result storage rpg:forge d.ns int 1 run scoreboard players get #need_s rpg_fg
execute store result storage rpg:forge d.nn int 1 run scoreboard players get #need_n rpg_fg
