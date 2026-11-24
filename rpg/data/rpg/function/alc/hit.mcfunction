advancement revoke @s only rpg:alc/hit
execute if score @s rpg_po_sh matches 1.. run effect clear @s minecraft:invisibility
execute if score @s rpg_po_sh matches 1.. run function rpg:alc/fx/shadow_off
execute if score @s rpg_po_bl matches 1.. at @s as @e[distance=0.1..6,type=!minecraft:player,type=!minecraft:item,type=!minecraft:item_display] if data entity @s {HurtTime:10s} run data merge entity @s {Fire:80s}
