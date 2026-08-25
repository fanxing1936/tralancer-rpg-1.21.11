scoreboard players add @s rpg_lt_divine 0
scoreboard players add @s rpg_lt_div_cd 0
scoreboard players add @s rpg_lt_div_max 0
scoreboard players add @s rpg_lt_div_t 0
scoreboard players add @s rpg_lt_regen 0
scoreboard players add @s rpg_lt_auth 0
scoreboard players add @s rpg_lt_claim 0
scoreboard players add @s rpg_lt_migrate 0
execute if score @s rpg_lt_div_cd matches 1.. if score @s rpg_lt_div_max matches ..0 if score @s rpg_lt_divine matches 1 run scoreboard players set @s rpg_lt_div_max 600
execute if score @s rpg_lt_div_cd matches 1.. if score @s rpg_lt_div_max matches ..0 if score @s rpg_lt_divine matches 2 run scoreboard players set @s rpg_lt_div_max 400
execute if score @s rpg_lt_div_cd matches 1.. run scoreboard players remove @s rpg_lt_div_cd 1
execute unless score @s rpg_lt_div_cd matches 1.. run scoreboard players set @s rpg_lt_div_max 0
execute if score @s rpg_lt_div_t matches 1.. run scoreboard players remove @s rpg_lt_div_t 1
execute if score @s rpg_lt_divine matches 1 run function rpg:divine/old_tick
execute if score @s rpg_lt_divine matches 2 run function rpg:divine/new_tick
execute if score @s rpg_lt_migrate matches 0 if score @s rpg_lt_covenant matches 1.. run function rpg:divine/migrate_legacy
