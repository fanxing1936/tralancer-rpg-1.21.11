$item replace entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents from entity @s $(s)
scoreboard players set #c rpg_dt 1
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents #minecraft:axes run scoreboard players set #c rpg_dt 2
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents minecraft:mace run scoreboard players set #c rpg_dt 3
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents #minecraft:spears run scoreboard players set #c rpg_dt 4
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents minecraft:trident run scoreboard players set #c rpg_dt 4
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents #minecraft:hoes run scoreboard players set #c rpg_dt 7
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents minecraft:bow run scoreboard players set #c rpg_dt 8
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents minecraft:crossbow run scoreboard players set #c rpg_dt 9
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents *[minecraft:custom_data~{forge_tag:1b}] run scoreboard players set #c rpg_dt 3
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents *[minecraft:custom_data~{michael_spine_tag:1b}] run scoreboard players set #c rpg_dt 5
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents *[minecraft:custom_data~{grave_bane_tag:1b}] run scoreboard players set #c rpg_dt 5
execute if items entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] contents *[minecraft:custom_data~{michael_rib_tag:1b}] run scoreboard players set #c rpg_dt 6
data modify storage rpg:daath t.e set value {c:1}
execute store result storage rpg:daath t.e.c int 1 run scoreboard players get #c rpg_dt
data modify storage rpg:daath t.e.item set from entity @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4,limit=1] item
function rpg:daath_fight/snap/push with storage rpg:daath t
