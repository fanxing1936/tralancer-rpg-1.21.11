execute in rpg:armageddon_4 run summon minecraft:vindicator -3 81 0 {Tags:["rpg.pr.actor","rpg.pr.a.lucifer","rpg.pr.w.lucifer","rpg.pr.new"],Rotation:[-90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_lucifer/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_4 run summon minecraft:vindicator -9.6 81 -7.4 {Tags:["rpg.pr.actor","rpg.pr.a.beelzebub","rpg.pr.w.beelzebub","rpg.pr.new"],Rotation:[-61.2f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_beelzebub/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_4 run summon minecraft:vindicator -13 81 2.8 {Tags:["rpg.pr.actor","rpg.pr.a.belial","rpg.pr.w.belial","rpg.pr.new"],Rotation:[-109.3f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_belial/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_4 run summon minecraft:vindicator -8.8 81 8 {Tags:["rpg.pr.actor","rpg.pr.a.mammon","rpg.pr.w.mammon","rpg.pr.new"],Rotation:[-119.7f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_mammon/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute in rpg:armageddon_4 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] -9.6 81 -7.4 -61.2 0
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_4 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -20.0 85.0 0.5 -90.0 6.0
