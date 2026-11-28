# 开局（as/at 玩家，宏 id）：护甲四格、副手、主手有东西就收起来，格子清空
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ob.tmp"]}
# 区块没载入、召不出临时实体：什么都不动（不能先清格子再存，存不进去东西就没了）
execute unless entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] run return 0
execute if items entity @s armor.head * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s armor.head
$execute if items entity @s armor.head * run data modify storage rpg:onboard p$(id).stash.head set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.head run item replace entity @s armor.head with minecraft:air
execute if items entity @s armor.chest * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s armor.chest
$execute if items entity @s armor.chest * run data modify storage rpg:onboard p$(id).stash.chest set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.chest run item replace entity @s armor.chest with minecraft:air
execute if items entity @s armor.legs * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s armor.legs
$execute if items entity @s armor.legs * run data modify storage rpg:onboard p$(id).stash.legs set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.legs run item replace entity @s armor.legs with minecraft:air
execute if items entity @s armor.feet * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s armor.feet
$execute if items entity @s armor.feet * run data modify storage rpg:onboard p$(id).stash.feet set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.feet run item replace entity @s armor.feet with minecraft:air
execute if items entity @s weapon.offhand * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s weapon.offhand
$execute if items entity @s weapon.offhand * run data modify storage rpg:onboard p$(id).stash.off set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.off run item replace entity @s weapon.offhand with minecraft:air
execute if items entity @s weapon.mainhand * run item replace entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] contents from entity @s weapon.mainhand
$execute if items entity @s weapon.mainhand * run data modify storage rpg:onboard p$(id).stash.main set from entity @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1] item
$execute if data storage rpg:onboard p$(id).stash.main run item replace entity @s weapon.mainhand with minecraft:air
kill @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1]
