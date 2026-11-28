scoreboard players set @s rpg_dm_exp 300
execute as @e[tag=rpg.tw.guard,distance=..16] at @s run particle minecraft:angry_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 3
playsound minecraft:entity.vindicator.celebrate hostile @a[distance=..24] ~ ~ ~ 1 0.7
tellraw @a[distance=..64] ["",{"text":"〖圣卫〗","color":"#C9A646","bold":true,"italic":false},{"text":"  罪器！拿下他——","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"〖林中营地〗","color":"#A276BE","bold":true,"italic":false},{"text":"  你在圣卫面前亮了罪器。五分钟内，你的名字挂在告示板的通缉令上。","color":"#FF6B5E","bold":false,"italic":false}]
