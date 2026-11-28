# 原质：记打过、给阅历（add_sephira.py）
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run function rpg:sephira/boss/michael
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run particle minecraft:flash{color:16765117} ~ ~2 ~ 0 0 0 0 1 force
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run particle minecraft:end_rod ~ ~4 ~ 3 3 3 0.02 60 force
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1 0.6
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run tellraw @a[distance=..48] ["",{"text":"〖犹大书 1:9〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"天使长米迦勒……尚且不敢用毁谤的话罪责他，只说：主责备你吧！","color":"#E6DFCF","bold":false,"italic":false}]
# 掉落（第 9 节第 5 条）：在场的人各得米迦勒脊骨、米迦勒肋骨一把
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] as @e[tag=rpg.unit.ns,distance=..48] run function rpg:command/give/michael
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run tellraw @a[distance=..48,gamemode=!spectator] ["",{"text":"〖米迦勒〗","color":"#FFD0BD","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"灵走了，骨留下来。你拾起了米迦勒脊骨与米迦勒肋骨。","color":"#9C9A94","bold":false,"italic":false}]
# 装备养成：希望之源与符石
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] run loot spawn ~ ~1 ~ loot rpg:forge/boss/hope
function rpg:michael_boss_i3/clear
