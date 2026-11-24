data modify storage rpg:onboard made set value {}
data modify storage rpg:onboard made.head set value {text:"—"}
data modify storage rpg:onboard made.chest set value {text:"—"}
data modify storage rpg:onboard made.legs set value {text:"—"}
data modify storage rpg:onboard made.feet set value {text:"—"}
data modify storage rpg:onboard made.offhand set value {text:"—"}
data modify storage rpg:onboard made.head set from entity @s equipment.head.components."minecraft:custom_name"
data modify storage rpg:onboard made.chest set from entity @s equipment.chest.components."minecraft:custom_name"
data modify storage rpg:onboard made.legs set from entity @s equipment.legs.components."minecraft:custom_name"
data modify storage rpg:onboard made.feet set from entity @s equipment.feet.components."minecraft:custom_name"
data modify storage rpg:onboard made.offhand set from entity @s equipment.offhand.components."minecraft:custom_name"
function rpg:onboard/tut/made_dlg with storage rpg:onboard made
