$data modify entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item set from storage rpg:onboard p$(id).stash.legs
item replace entity @s armor.legs from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents
