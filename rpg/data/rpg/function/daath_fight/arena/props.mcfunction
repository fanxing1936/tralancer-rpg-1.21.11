# 场次开始：中心标记与十盏灯（positioned 场地中心）
kill @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..60]
kill @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.c"]}
summon minecraft:interaction ~0 ~ ~-20 {Tags:["rpg.dt.lamp","rpg.dt.l0"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~11 ~ ~-16 {Tags:["rpg.dt.lamp","rpg.dt.l1"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~19 ~ ~-6 {Tags:["rpg.dt.lamp","rpg.dt.l2"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~19 ~ ~6 {Tags:["rpg.dt.lamp","rpg.dt.l3"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~11 ~ ~16 {Tags:["rpg.dt.lamp","rpg.dt.l4"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~0 ~ ~20 {Tags:["rpg.dt.lamp","rpg.dt.l5"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~-11 ~ ~16 {Tags:["rpg.dt.lamp","rpg.dt.l6"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~-19 ~ ~6 {Tags:["rpg.dt.lamp","rpg.dt.l7"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~-19 ~ ~-6 {Tags:["rpg.dt.lamp","rpg.dt.l8"],width:1.5f,height:4.2f,response:1b}
summon minecraft:interaction ~-11 ~ ~-16 {Tags:["rpg.dt.lamp","rpg.dt.l9"],width:1.5f,height:4.2f,response:1b}
function rpg:daath_fight/arena/tree
