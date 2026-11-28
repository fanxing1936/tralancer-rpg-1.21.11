# 座天使（at 它的中心）
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.pr.throne","rpg.pr.ent","rpg.pr.w.throne","rpg.pr.new"],NoAI:1b,NoGravity:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,Rotation:[0f,0f],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_throne/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
scoreboard players set #thr rpg_pr_i3 0
scoreboard players set #first rpg_pr_i3 0
summon minecraft:slime ~0 ~1.55 ~0 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w0"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-2.65 ~0 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w1"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-0.65 ~2.4 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w2"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-0.65 ~-2.4 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w3"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..] run attribute @s minecraft:max_health base set 10
execute as @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..] run data merge entity @s {Health:10f}
playsound minecraft:block.beacon.activate master @a[tag=rpg.pri3] ~ ~ ~ 2 1.4
