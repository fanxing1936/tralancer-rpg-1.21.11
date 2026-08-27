scoreboard players add @s rpg_ex_hud_t 0
execute if score @s rpg_ex_hud_t matches 1.. run scoreboard players remove @s rpg_ex_hud_t 1
scoreboard players add @s rpg_ex_usecd 0
execute if score @s rpg_ex_usecd matches 1.. run scoreboard players remove @s rpg_ex_usecd 1
scoreboard players enable @s rpg_ex_choice
scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_ex_lvl 0
scoreboard players add @s rpg_ex_path 0
scoreboard players add @s rpg_ex_seen 0
execute unless score @s rpg_ex_xp = @s rpg_ex_seen run function rpg:inquest/career/sync
execute if score @s rpg_ex_lvl matches 0 run function rpg:inquest/career/sync
execute if score @s rpg_ex_choice matches 1..4 run function rpg:inquest/choice/final
execute if score @s rpg_ex_choice matches 11..13 run function rpg:inquest/choice/ransom
execute if score @s rpg_ex_choice matches 21 run function rpg:inquest/career/choose1
execute if score @s rpg_ex_choice matches 22 run function rpg:inquest/career/choose2
execute if score @s rpg_ex_choice matches 23 run function rpg:inquest/career/choose3
execute if score @s rpg_ex_choice matches 1.. run scoreboard players set @s rpg_ex_choice 0
execute if score @s rpg_ex_use matches 1.. if items entity @s weapon.mainhand minecraft:goat_horn[minecraft:custom_data~{rpg_bell:1b}] run function rpg:inquest/tool/bell
execute if score @s rpg_ex_use matches 1.. run scoreboard players set @s rpg_ex_use 0
function rpg:inquest/seal/player_tick

function rpg:panel/tick
