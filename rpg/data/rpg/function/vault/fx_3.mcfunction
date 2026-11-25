# 传说
particle minecraft:dust{color:[1.00,0.67,0.00],scale:1.6} ~ ~0.6 ~ 0.35 0.5 0.35 0 36
title @a[tag=rpg.vt.op] times 4 30 12
title @a[tag=rpg.vt.op] title {"text":""}
title @a[tag=rpg.vt.op] subtitle ["",{"text":"传说　","color":"#FFAA00","bold":true,"italic":false},{"text":"𝔏𝔢𝔤𝔢𝔫𝔡","color":"#8F7430","italic":false}]
particle minecraft:flash{color:[1.00,0.67,0.00,1.0]} ~ ~0.7 ~ 0 0 0 0 1
particle minecraft:end_rod ~ ~0.6 ~ 0.1 0.1 0.1 0.14 36
playsound minecraft:item.totem.use block @a[distance=..24] ~ ~ ~ 0.35 1.5
playsound minecraft:block.bell.resonate block @a[distance=..24] ~ ~ ~ 1 1.1
particle minecraft:dust{color:[1.00,0.67,0.00],scale:2.2} ~ ~4 ~ 0.12 3.2 0.12 0 90
playsound minecraft:ui.toast.challenge_complete block @a[distance=..32] ~ ~ ~ 0.9 1
summon minecraft:firework_rocket ~ ~1.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:0,explosions:[{shape:"large_ball",has_twinkle:1b,has_trail:1b,colors:[I;16755200,16777215],fade_colors:[I;16755200]}]}}}}
tellraw @a[distance=..64] ["",{"text":"〖失乐园・宝库〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔙𝔞𝔲𝔩𝔱","color":"#8F7430","italic":false},{"text":"  ","italic":false},{"selector":"@a[tag=rpg.vt.op,limit=1]","color":"#E6DFCF"},{"text":" 抽到了 ","color":"#9C9A94","italic":false},{"storage":"rpg:vault","nbt":"n","interpret":true}]
