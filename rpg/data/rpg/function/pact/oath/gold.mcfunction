# 玛门的供奉：一次最多献 16 个金锭，每个 2 点契合。
execute store result score #c rpg_pact run clear @s minecraft:gold_ingot[!minecraft:custom_data] 16
execute if score #c rpg_pact matches ..0 run return run function rpg:pact/say/no_gold
scoreboard players operation #gain rpg_pact = #c rpg_pact
scoreboard players operation #gain rpg_pact *= #two rpg_pact
function rpg:pact/oath/gain
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2
