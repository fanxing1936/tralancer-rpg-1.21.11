scoreboard players operation #q rpg_vt = @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=9},limit=1] rpg_vt_q
data modify storage rpg:vault i set from entity @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6,scores={rpg_vt_k=9},limit=1] item
function rpg:vault/show
