# 契合归零。一阶没有可掉的，魔神直接往里压。
execute if score @s rpg_pact_lv matches ..1 run scoreboard players add @s rpg_taint 20
execute if score @s rpg_pact_lv matches ..1 run return run scoreboard players set @s rpg_pact_bond 30
scoreboard players remove @s rpg_pact_lv 1
scoreboard players set @s rpg_pact_bond 50
function rpg:pact/attr
function rpg:pact/seal/trim
function rpg:pact/book/resync
function rpg:hud/m91
playsound minecraft:block.glass.break player @s ~ ~ ~ 1 0.5
