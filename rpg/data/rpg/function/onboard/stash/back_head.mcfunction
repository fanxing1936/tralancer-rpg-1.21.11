$data modify entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item set from storage rpg:onboard p$(id).stash.head
item replace entity @s armor.head from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents
