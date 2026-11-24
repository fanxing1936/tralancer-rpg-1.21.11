function rpg:events/place_near
scoreboard players set #ev rpg_ev 6
scoreboard players operation #end rpg_ev = #now rpg_ev
scoreboard players add #end rpg_ev 6000
data modify storage rpg:events cur.n set value "迷途商人"
execute store result storage rpg:events cur.x int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[0]
execute store result storage rpg:events cur.z int 1 run data get entity @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] Pos[2]
execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:merchant/place/travel
execute at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run tag @e[type=minecraft:villager,tag=rpg.mer.travel,distance=..1,limit=1,sort=nearest] add rpg.mer.temp
tellraw @a ["",{"text":"〖事件・迷途商人〗","color":"#FFF2A8","bold":true,"italic":false},{"text":" 𝔗𝔯𝔞𝔳𝔢𝔩𝔩𝔦𝔫𝔤 𝔐𝔢𝔯𝔠𝔥𝔞𝔫𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  一位迷途商人在附近歇脚，只待 5 分钟。","color":"#9C9A94","bold":false,"italic":false},{"text":"　坐标 ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.x","storage":"rpg:events","color":"#E6DFCF","bold":false,"italic":false},{"text":", ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.z","storage":"rpg:events","color":"#E6DFCF","bold":false,"italic":false}]
