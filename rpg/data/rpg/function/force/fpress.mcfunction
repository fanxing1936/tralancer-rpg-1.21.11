# 按了 F：两只手换回来（哪一边都可能是锻造武器，原样放回），再放 Ⅲ 号槽 / Shift+F 开技能页
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fo.tmp"]}
item replace entity @e[type=minecraft:item_display,tag=rpg.fo.tmp,limit=1,sort=nearest] contents from entity @s weapon.mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand from entity @e[type=minecraft:item_display,tag=rpg.fo.tmp,limit=1,sort=nearest] contents
kill @e[type=minecraft:item_display,tag=rpg.fo.tmp]
scoreboard players operation #fm rpg_fo = @s rpg_fo_pm
scoreboard players operation #fo rpg_fo = @s rpg_fo_po
scoreboard players operation #tree rpg_fo = #fm rpg_fo
execute if score #tree rpg_fo matches 0 run scoreboard players operation #tree rpg_fo = #fo rpg_fo
execute if score #tree rpg_fo matches 3 run return run function rpg:pact/fkey
execute if predicate rpg:sneaking run return run function rpg:force/page/by_tree
scoreboard players set #slot rpg_fo 3
function rpg:force/cast
