scoreboard players set #sq_stance rpg_squad 1
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 1
function rpg:hud/m29
playsound minecraft:block.anvil_land player @s ~ ~ ~ 0.5 1.6
