tag @s add rpg.dt.face
execute as @a[tag=rpg.dt.me,limit=1] run loot replace entity @e[type=minecraft:item_display,tag=rpg.dt.face,limit=1] contents loot rpg:daath/head
tag @s remove rpg.dt.face
data modify entity @s item.components."minecraft:item_model" set value "rpg:daath/face"
data modify entity @s item_display set value "fixed"
