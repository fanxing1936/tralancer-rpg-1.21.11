# 史诗
particle minecraft:dust{color:[0.72,0.36,0.94],scale:1.6} ~ ~0.6 ~ 0.35 0.5 0.35 0 28
title @a[tag=rpg.vt.op] times 4 30 12
title @a[tag=rpg.vt.op] title {"text":""}
title @a[tag=rpg.vt.op] subtitle ["",{"text":"史诗　","color":"#B85CF0","bold":true,"italic":false},{"text":"𝔈𝔭𝔦𝔠","color":"#8F7430","italic":false}]
particle minecraft:flash{color:[0.72,0.36,0.94,1.0]} ~ ~0.7 ~ 0 0 0 0 1
particle minecraft:end_rod ~ ~0.6 ~ 0.1 0.1 0.1 0.14 24
playsound minecraft:item.totem.use block @a[distance=..24] ~ ~ ~ 0.35 1.5
playsound minecraft:block.bell.resonate block @a[distance=..24] ~ ~ ~ 1 1.0
