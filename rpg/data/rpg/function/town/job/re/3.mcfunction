# 重修 波斯拉：原址（#x/#z）、原高度（出生点锚的 y）、原地皮
execute unless score #sy3 rpg_tw matches 1.. run return run scoreboard players set #s3 rpg_tw 3
scoreboard players set #cur rpg_tw 3
scoreboard players operation #px rpg_tw = #x3 rpg_tw
scoreboard players operation #pz rpg_tw = #z3 rpg_tw
scoreboard players operation #v rpg_tw = #v3 rpg_tw
scoreboard players operation #h0 rpg_tw = #sy3 rpg_tw
scoreboard players set #r rpg_tw 159
function rpg:town/job/coords
function rpg:town/job/bigcoords
function rpg:town/job/big_add with storage rpg:town m
scoreboard players set #wt rpg_tw 0
scoreboard players set #ph rpg_tw 4
