# 「用我的游戏名」
execute unless score #do rpg_ob matches 2 run return 0
loot replace entity @s weapon.mainhand loot rpg:onboard/head_of
data modify storage rpg:onboard tmp.n set from entity @s SelectedItem.components."minecraft:profile".name
item replace entity @s weapon.mainhand with minecraft:air
execute unless data storage rpg:onboard tmp.n run data modify storage rpg:onboard tmp.n set value "无名旅人"
function rpg:onboard/name/keep
