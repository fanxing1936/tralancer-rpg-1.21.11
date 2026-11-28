# 最后一片羽毛：米迦勒 Boss 现成的羽毛模型，转着飘下来
execute in rpg:armageddon run summon minecraft:item_display 0 99 -2 {Tags:["rpg.pr.feather","rpg.pr.ent"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:prologue_feather"}},item_display:"fixed",teleport_duration:59,Rotation:[0f,0f]}
schedule function rpg:prologue_i1/_sched/cut/feather_fall 2t
