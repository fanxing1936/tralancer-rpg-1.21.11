execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/showoff
execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" 𝔊𝔢𝔫𝔢𝔰𝔦𝔰 2:23","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"骨中之骨 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"骨中之骨。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 1.6 0.8
execute on passengers if entity @s[tag=rpg.mkm.p.rib] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.mkm.p.rib_attack] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute rotated 90 0 positioned ^ ^ ^4 run function rpg:michael_boss_i3/bones/orbit {side:"a"}
execute rotated -90 0 positioned ^ ^ ^4 run function rpg:michael_boss_i3/bones/orbit {side:"b"}
summon minecraft:marker ~ ~ ~9.17 {Tags:["rpg.mkb.fx","rpg.mkb.bp1"]}
summon minecraft:marker ~ ~ ~-9.17 {Tags:["rpg.mkb.fx","rpg.mkb.bp2"]}
scoreboard players set @e[tag=rpg.mkb.bp1,distance=0..] rpg_mk_life 164
scoreboard players set @e[tag=rpg.mkb.bp2,distance=0..] rpg_mk_life 164
scoreboard players set @e[tag=rpg.mkb.bp1,distance=0..] rpg_mk_kd 0
scoreboard players set @e[tag=rpg.mkb.bp2,distance=0..] rpg_mk_kd 0
