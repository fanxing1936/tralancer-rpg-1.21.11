# Integration template; root owns actual objective/storage and tick hooks.
# Initial item component: minecraft:custom_model_data={colors:[16777215,2478848,2544384]}
scoreboard players add #phase rpg.lu2_mat 1
execute if score #phase rpg.lu2_mat matches 200.. run scoreboard players set #phase rpg.lu2_mat 0
scoreboard players set #color rpg.lu2_mat 2544384
scoreboard players operation #color rpg.lu2_mat += #phase rpg.lu2_mat
execute store result storage rpg:lucifer_p2 material.glow_color int 1 run scoreboard players get #color rpg.lu2_mat
execute as @e[type=minecraft:item_display,tag=rpg.lu2.pulse] run data modify entity @s item.components."minecraft:custom_model_data".colors[2] set from storage rpg:lucifer_p2 material.glow_color
