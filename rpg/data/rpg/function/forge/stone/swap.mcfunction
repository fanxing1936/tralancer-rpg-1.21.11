# 潜行按 F 照常换手（比如要把武器放到副手进工坊）。
execute if predicate rpg:forge/sneaking run return 0
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.fg.tmp"],view_range:0f}
item replace entity @e[type=minecraft:item_display,tag=rpg.fg.tmp,limit=1] contents from entity @s weapon.mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand from entity @e[type=minecraft:item_display,tag=rpg.fg.tmp,limit=1] contents
kill @e[type=minecraft:item_display,tag=rpg.fg.tmp]
scoreboard players set #cast rpg_fg 1
