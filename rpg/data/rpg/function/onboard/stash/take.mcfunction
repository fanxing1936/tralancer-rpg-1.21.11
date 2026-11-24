# 结束（as/at 玩家，宏 id）
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.ob.tmp"]}
$execute if data storage rpg:onboard p$(id).stash.head if items entity @s armor.head * run function rpg:onboard/stash/drop_head
$execute if data storage rpg:onboard p$(id).stash.head run function rpg:onboard/stash/back_head with storage rpg:onboard tmp
$execute if data storage rpg:onboard p$(id).stash.chest if items entity @s armor.chest * run function rpg:onboard/stash/drop_chest
$execute if data storage rpg:onboard p$(id).stash.chest run function rpg:onboard/stash/back_chest with storage rpg:onboard tmp
$execute if data storage rpg:onboard p$(id).stash.legs if items entity @s armor.legs * run function rpg:onboard/stash/drop_legs
$execute if data storage rpg:onboard p$(id).stash.legs run function rpg:onboard/stash/back_legs with storage rpg:onboard tmp
$execute if data storage rpg:onboard p$(id).stash.feet if items entity @s armor.feet * run function rpg:onboard/stash/drop_feet
$execute if data storage rpg:onboard p$(id).stash.feet run function rpg:onboard/stash/back_feet with storage rpg:onboard tmp
# 教学武器在副手：主手原来空着就交到主手，否则掉在脚边
$execute if data storage rpg:onboard p$(id).stash.main if items entity @s weapon.offhand * run function rpg:onboard/stash/drop_off
$execute unless data storage rpg:onboard p$(id).stash.main run item replace entity @s weapon.mainhand from entity @s weapon.offhand
$execute unless data storage rpg:onboard p$(id).stash.main run item replace entity @s weapon.offhand with minecraft:air
$execute if data storage rpg:onboard p$(id).stash.main run function rpg:onboard/stash/back_main with storage rpg:onboard tmp
$execute if data storage rpg:onboard p$(id).stash.off if items entity @s weapon.offhand * run function rpg:onboard/stash/drop_off
$execute if data storage rpg:onboard p$(id).stash.off run function rpg:onboard/stash/back_off with storage rpg:onboard tmp
$data remove storage rpg:onboard p$(id).stash
kill @e[type=minecraft:item_display,tag=rpg.ob.tmp,distance=..3,limit=1]
