execute in rpg:armageddon_2 run summon minecraft:vindicator 4 121 0 {Tags:["rpg.pr.actor","rpg.pr.a.michael","rpg.pr.w.michael","rpg.pr.new"],Rotation:[90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_michael/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_2 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] 4 121 0 90 0
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -2.0 82.2 -3.5 -60.0 -62.0
