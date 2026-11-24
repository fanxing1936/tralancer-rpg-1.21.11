$data modify entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item set from storage rpg:onboard p$(id).stash.feet
item replace entity @s armor.feet from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents
