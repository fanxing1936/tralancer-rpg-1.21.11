execute if score @s rpg_mk_t matches 1..60 run particle minecraft:end_rod ~ ~2 ~ 1.2 1 1.2 0.02 2
execute if score @s rpg_mk_t matches 4 run function rpg:michael_boss/gaze/ring1
execute if score @s rpg_mk_t matches 5 run execute as @e[tag=rpg.mkb.eye1] at @s run tp @s ^ ^0.2 ^6
execute if score @s rpg_mk_t matches 4 run playsound minecraft:entity.elder_guardian.ambient hostile @a[distance=..48] ~ ~ ~ 1 1.4
execute if score @s rpg_mk_t matches 47 run execute as @e[tag=rpg.mkb.eye1] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 50 run execute as @e[tag=rpg.mkb.eye1] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 4 run function rpg:michael_boss/gaze/floor1
execute if score @s rpg_mk_t matches 16 run function rpg:michael_boss/gaze/ring2
execute if score @s rpg_mk_t matches 17 run execute as @e[tag=rpg.mkb.eye2] at @s run tp @s ^ ^1.0 ^14
execute if score @s rpg_mk_t matches 16 run playsound minecraft:entity.elder_guardian.ambient hostile @a[distance=..48] ~ ~ ~ 1 1.2
execute if score @s rpg_mk_t matches 50 run execute as @e[tag=rpg.mkb.eye2] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 53 run execute as @e[tag=rpg.mkb.eye2] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 16 run function rpg:michael_boss/gaze/floor2
execute if score @s rpg_mk_t matches 28 run function rpg:michael_boss/gaze/ring3
execute if score @s rpg_mk_t matches 29 run execute as @e[tag=rpg.mkb.eye3] at @s run tp @s ^ ^2.2 ^24
execute if score @s rpg_mk_t matches 28 run playsound minecraft:entity.elder_guardian.ambient hostile @a[distance=..48] ~ ~ ~ 1 1.0
execute if score @s rpg_mk_t matches 53 run execute as @e[tag=rpg.mkb.eye3] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 56 run execute as @e[tag=rpg.mkb.eye3] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 28 run function rpg:michael_boss/gaze/floor3
execute if score @s rpg_mk_t matches 1 run function rpg:michael_boss/gaze/seal
execute if score @s rpg_mk_t matches 50 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"不可直视。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_t matches 60 run execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 61 run execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 65 run execute as @e[tag=rpg.mkb.eye] run data modify entity @s text set value {text:"",font:"rpg:michael_vfx",color:"white"}
execute if score @s rpg_mk_t matches 60 run function rpg:michael_boss/gaze/burst
execute if score @s rpg_mk_t matches 20 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 20 run title @a[distance=..48] times 6 30 0
execute if score @s rpg_mk_t matches 20 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 38 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 38 run title @a[distance=..48] times 0 30 0
execute if score @s rpg_mk_t matches 38 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 52 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 52 run title @a[distance=..48] times 0 12 0
execute if score @s rpg_mk_t matches 52 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 62 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 62 run title @a[distance=..48] times 0 3 0
execute if score @s rpg_mk_t matches 62 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 64 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 64 run title @a[distance=..48] times 0 3 0
execute if score @s rpg_mk_t matches 64 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 66 run title @a[distance=..48] clear
execute if score @s rpg_mk_t matches 66 run title @a[distance=..48] times 0 2 12
execute if score @s rpg_mk_t matches 66 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_t matches 72 run execute as @e[tag=rpg.mkb.eye] at @s run function rpg:michael_boss/gaze/fade
execute if score @s rpg_mk_t matches 82.. run function rpg:michael_boss/sk/end
