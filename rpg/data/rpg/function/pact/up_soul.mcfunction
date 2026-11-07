execute store result score #c rpg_pact run clear @s minecraft:iron_nugget[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..3 run return run function rpg:pact/say/up_items
execute store result score #c rpg_pact run clear @s minecraft:arrow[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..3 run return run function rpg:pact/say/up_items
execute store result score #c rpg_pact run clear @s minecraft:glowstone_dust[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..3 run return run function rpg:pact/say/up_items
execute store result score #c rpg_pact run clear @s minecraft:spider_eye[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..3 run return run function rpg:pact/say/up_items
execute store result score #c rpg_pact run clear @s minecraft:redstone[!minecraft:custom_data] 0
execute if score #c rpg_pact matches ..3 run return run function rpg:pact/say/up_items
clear @s minecraft:iron_nugget[!minecraft:custom_data] 4
clear @s minecraft:arrow[!minecraft:custom_data] 4
clear @s minecraft:glowstone_dust[!minecraft:custom_data] 4
clear @s minecraft:spider_eye[!minecraft:custom_data] 4
clear @s minecraft:redstone[!minecraft:custom_data] 4
function rpg:pact/up_done
