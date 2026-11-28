execute positioned ~1 ~ ~1 run function rpg:town/prop {n:"crate_pile"}
$summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.trace","rpg.te.tr$(n)"],width:1.2f,height:1.4f,response:1b}
summon minecraft:item_display ~ ~0.4 ~ {Tags:["rpg.tw.ev"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:town/fx_flies"}},billboard:"center"}
