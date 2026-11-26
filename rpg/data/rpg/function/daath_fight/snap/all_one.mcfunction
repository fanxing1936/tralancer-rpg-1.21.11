# 主手那把存进 t.e（as/at 挑战者）
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.tmp"]}
data modify storage rpg:daath t.keep set from storage rpg:daath t.n
data modify storage rpg:daath t.n set value 0
data modify storage rpg:daath s0.arms set value []
function rpg:daath_fight/snap/one {s:"weapon.mainhand"}
kill @e[type=minecraft:item_display,tag=rpg.dt.tmp,distance=..4]
