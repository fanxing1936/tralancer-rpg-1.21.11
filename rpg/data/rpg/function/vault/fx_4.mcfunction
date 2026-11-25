# 限定
particle minecraft:dust{color:[1.00,0.84,0.00],scale:1.6} ~ ~0.6 ~ 0.35 0.5 0.35 0 44
title @a[tag=rpg.vt.op] times 4 30 12
title @a[tag=rpg.vt.op] title {"text":""}
title @a[tag=rpg.vt.op] subtitle ["",{"text":"限定　","color":"#FFD700","bold":true,"italic":false},{"text":"𝔏𝔦𝔪𝔦𝔱𝔢𝔡","color":"#8F7430","italic":false}]
particle minecraft:flash{color:[1.00,0.84,0.00,1.0]} ~ ~0.7 ~ 0 0 0 0 1
particle minecraft:end_rod ~ ~0.6 ~ 0.1 0.1 0.1 0.14 48
playsound minecraft:item.totem.use block @a[distance=..24] ~ ~ ~ 0.35 1.5
playsound minecraft:block.bell.resonate block @a[distance=..24] ~ ~ ~ 1 1.2
particle minecraft:dust{color:[1.00,0.84,0.00],scale:2.2} ~ ~4 ~ 0.12 3.2 0.12 0 90
playsound minecraft:ui.toast.challenge_complete block @a[distance=..32] ~ ~ ~ 0.9 1
summon minecraft:firework_rocket ~ ~1.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:0,explosions:[{shape:"large_ball",has_twinkle:1b,has_trail:1b,colors:[I;16766720,16777215],fade_colors:[I;16766720]}]}}}}
tellraw @a[distance=..64] ["",{"text":"〖失乐园・宝库〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔙𝔞𝔲𝔩𝔱","color":"#8F7430","italic":false},{"text":"  ","italic":false},{"selector":"@a[tag=rpg.vt.op,limit=1]","color":"#E6DFCF"},{"text":" 抽到了 ","color":"#9C9A94","italic":false},{"storage":"rpg:vault","nbt":"n","interpret":true}]
playsound minecraft:entity.lightning_bolt.thunder block @a[distance=..48] ~ ~ ~ 0.7 1.2
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.5 60
