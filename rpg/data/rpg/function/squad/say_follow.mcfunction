scoreboard players set #sq_stance rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players set @s rpg_sq_mode 0
function rpg:hud/m28
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1.3
