execute in rpg:armageddon_2 run summon minecraft:vindicator 0 90 0 {Tags:["rpg.pr.actor","rpg.pr.a.lucifer","rpg.pr.w.lucifer","rpg.pr.new"],Rotation:[-90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_lucifer/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_2 run summon minecraft:vindicator -3.6 81 -5.2 {Tags:["rpg.pr.actor","rpg.pr.a.beelzebub","rpg.pr.w.beelzebub","rpg.pr.new"],Rotation:[-16.7f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_beelzebub/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_2 run summon minecraft:vindicator -7.2 81 1 {Tags:["rpg.pr.actor","rpg.pr.a.belial","rpg.pr.w.belial","rpg.pr.new"],Rotation:[-111.9f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_belial/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_2 run summon minecraft:vindicator -2.8 81 4.8 {Tags:["rpg.pr.actor","rpg.pr.a.mammon","rpg.pr.w.mammon","rpg.pr.new"],Rotation:[-175.7f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_mammon/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_2 run summon minecraft:vindicator 8 94 0 {Tags:["rpg.pr.actor","rpg.pr.a.michael","rpg.pr.w.michael","rpg.pr.new"],Rotation:[90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_michael/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute as @a[tag=rpg.pri2] at @s run playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 1 0.5
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -7.0 84.0 5.0 -125.5 -38.3
