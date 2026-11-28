$execute unless data storage rpg:town keep.p$(id)[0] run return 0
summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:stone",count:1},Tags:["rpg.tl.ri"],PickupDelay:0s}
$data modify entity @e[type=minecraft:item,tag=rpg.tl.ri,limit=1] Item set from storage rpg:town keep.p$(id)[0]
tag @e[type=minecraft:item,tag=rpg.tl.ri] remove rpg.tl.ri
$data remove storage rpg:town keep.p$(id)[0]
scoreboard players add #n rpg_tl 1
$execute if score #n rpg_tl matches ..80 run function rpg:town/life/regive1 {id:$(id)}
