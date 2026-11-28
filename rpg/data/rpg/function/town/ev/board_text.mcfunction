# 告示板上今晚的副本（as 玩家，#t = 镇号）→ rpg:town ev.name / ev.hint
scoreboard players set #k rpg_te 0
execute if score #t rpg_tl matches 1 run scoreboard players operation #k rpg_te = #ev1 rpg_te
execute if score #t rpg_tl matches 1 if score #es1 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 2 run scoreboard players operation #k rpg_te = #ev2 rpg_te
execute if score #t rpg_tl matches 2 if score #es2 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 3 run scoreboard players operation #k rpg_te = #ev3 rpg_te
execute if score #t rpg_tl matches 3 if score #es3 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 4 run scoreboard players operation #k rpg_te = #ev4 rpg_te
execute if score #t rpg_tl matches 4 if score #es4 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 5 run scoreboard players operation #k rpg_te = #ev5 rpg_te
execute if score #t rpg_tl matches 5 if score #es5 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 6 run scoreboard players operation #k rpg_te = #ev6 rpg_te
execute if score #t rpg_tl matches 6 if score #es6 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 7 run scoreboard players operation #k rpg_te = #ev7 rpg_te
execute if score #t rpg_tl matches 7 if score #es7 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 8 run scoreboard players operation #k rpg_te = #ev8 rpg_te
execute if score #t rpg_tl matches 8 if score #es8 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 9 run scoreboard players operation #k rpg_te = #ev9 rpg_te
execute if score #t rpg_tl matches 9 if score #es9 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 10 run scoreboard players operation #k rpg_te = #ev10 rpg_te
execute if score #t rpg_tl matches 10 if score #es10 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 11 run scoreboard players operation #k rpg_te = #ev11 rpg_te
execute if score #t rpg_tl matches 11 if score #es11 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 12 run scoreboard players operation #k rpg_te = #ev12 rpg_te
execute if score #t rpg_tl matches 12 if score #es12 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 13 run scoreboard players operation #k rpg_te = #ev13 rpg_te
execute if score #t rpg_tl matches 13 if score #es13 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 14 run scoreboard players operation #k rpg_te = #ev14 rpg_te
execute if score #t rpg_tl matches 14 if score #es14 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 15 run scoreboard players operation #k rpg_te = #ev15 rpg_te
execute if score #t rpg_tl matches 15 if score #es15 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 16 run scoreboard players operation #k rpg_te = #ev16 rpg_te
execute if score #t rpg_tl matches 16 if score #es16 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 17 run scoreboard players operation #k rpg_te = #ev17 rpg_te
execute if score #t rpg_tl matches 17 if score #es17 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 18 run scoreboard players operation #k rpg_te = #ev18 rpg_te
execute if score #t rpg_tl matches 18 if score #es18 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 19 run scoreboard players operation #k rpg_te = #ev19 rpg_te
execute if score #t rpg_tl matches 19 if score #es19 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #t rpg_tl matches 20 run scoreboard players operation #k rpg_te = #ev20 rpg_te
execute if score #t rpg_tl matches 20 if score #es20 rpg_te matches 1.. run scoreboard players set #k rpg_te 9
execute if score #k rpg_te matches 1 run data modify storage rpg:town ev set value {name:"别西卜降临",hint:"粮仓里的麦子发黑了。神父说今晚要做一场驱魔。",icon:"rpg:town/ev_granary"}
execute if score #k rpg_te matches 2 run data modify storage rpg:town ev set value {name:"空缺者事件",hint:"墓地的土是松的。夜里有人看见没有脸的人。",icon:"rpg:town/ev_hollow"}
execute if score #k rpg_te matches 3 run data modify storage rpg:town ev set value {name:"女巫处刑",hint:"审判官进了城，广场上搭起了刑台。明早要烧女巫。",icon:"rpg:town/ev_witch"}
execute if score #k rpg_te matches 0 run data modify storage rpg:town ev set value {name:"（还没定）",hint:"今天的风声还没传开。",icon:"rpg:town/holy_fire"}
execute if score #k rpg_te matches 9 run data modify storage rpg:town ev set value {name:"今天的已经过去了",hint:"明天还会有事。",icon:"rpg:town/holy_fire"}
