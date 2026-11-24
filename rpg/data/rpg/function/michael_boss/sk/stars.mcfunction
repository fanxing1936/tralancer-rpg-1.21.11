execute if score @s rpg_mk_t matches 2..11 run tp @s ~ ~0.5 ~
execute if score @s rpg_mk_t matches 20 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn0
execute if score @s rpg_mk_t matches 32..48 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor0
execute if score @s rpg_mk_t matches 50 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit0
execute if score @s rpg_mk_t matches 20 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn1
execute if score @s rpg_mk_t matches 32..48 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor1
execute if score @s rpg_mk_t matches 50 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit1
execute if score @s rpg_mk_t matches 20 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn2
execute if score @s rpg_mk_t matches 32..48 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor2
execute if score @s rpg_mk_t matches 50 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit2
execute if score @s rpg_mk_t matches 20 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 70 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn0
execute if score @s rpg_mk_t matches 82..98 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor0
execute if score @s rpg_mk_t matches 100 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit0
execute if score @s rpg_mk_t matches 70 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn1
execute if score @s rpg_mk_t matches 82..98 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor1
execute if score @s rpg_mk_t matches 100 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit1
execute if score @s rpg_mk_t matches 70 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn2
execute if score @s rpg_mk_t matches 82..98 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor2
execute if score @s rpg_mk_t matches 100 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit2
execute if score @s rpg_mk_t matches 70 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 120 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn0
execute if score @s rpg_mk_t matches 132..148 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor0
execute if score @s rpg_mk_t matches 150 run execute if score @s rpg_mk_r matches 1 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit0
execute if score @s rpg_mk_t matches 120 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn1
execute if score @s rpg_mk_t matches 132..148 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor1
execute if score @s rpg_mk_t matches 150 run execute if score @s rpg_mk_r matches 2 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit1
execute if score @s rpg_mk_t matches 120 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/warn2
execute if score @s rpg_mk_t matches 132..148 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/meteor2
execute if score @s rpg_mk_t matches 150 run execute if score @s rpg_mk_r matches 0 at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/hit2
execute if score @s rpg_mk_t matches 120 run function rpg:michael/anim/enter/horn
execute if score @s rpg_mk_t matches 170 run execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/bigwarn
execute if score @s rpg_mk_t matches 170 run execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……最后一颗。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_t matches 190 run execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] run function rpg:michael_boss/stars/bighit
execute if score @s rpg_mk_t matches 196 run tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1]
execute if score @s rpg_mk_t matches 196 run data merge entity @s {NoGravity:0b}
execute if score @s rpg_mk_t matches 196 run tag @s remove rpg.mkb.air
execute if score @s rpg_mk_t matches 196 run function rpg:michael/anim/enter/land
execute if score @s rpg_mk_t matches 198 run function rpg:michael_boss/solid/on
execute if score @s rpg_mk_t matches 198 run scoreboard players set @s rpg_mk_so 40
execute if score @s rpg_mk_t matches 198 run function rpg:michael/anim/enter/idle
execute if score @s rpg_mk_t matches 238.. run function rpg:michael_boss/sk/end
