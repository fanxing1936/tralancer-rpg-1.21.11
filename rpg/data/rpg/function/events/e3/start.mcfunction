function rpg:events/place
function rpg:events/e3/begin
execute store result score #pp rpg_ev run random value 1..7
execute if score #pp rpg_ev matches 1 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_1
execute if score #pp rpg_ev matches 2 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_2
execute if score #pp rpg_ev matches 3 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_3
execute if score #pp rpg_ev matches 4 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_4
execute if score #pp rpg_ev matches 5 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_5
execute if score #pp rpg_ev matches 6 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_6
execute if score #pp rpg_ev matches 7 at @e[type=minecraft:marker,tag=rpg.ev.mk,limit=1] run function rpg:events/e3/spawn_7
tellraw @a ["",{"text":"〖事件・罪仆巡逻〗","color":"#A276BE","bold":true,"italic":false},{"text":" 𝔊𝔬𝔢𝔱𝔦𝔠 𝔓𝔞𝔱𝔯𝔬𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"一队罪仆在附近游荡。","color":"#9C9A94","bold":false,"italic":false},{"text":"　坐标 ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.x","storage":"rpg:events","color":"#E6DFCF"},{"text":", ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.z","storage":"rpg:events","color":"#E6DFCF"}]
playsound minecraft:entity.evoker.prepare_summon master @a ~ ~ ~ 1 0.6
