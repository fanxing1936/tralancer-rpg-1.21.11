summon minecraft:slime ~0 ~1.55 ~0 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w0"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-2.65 ~0 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w1"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-0.65 ~2.4 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w2"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
summon minecraft:slime ~0 ~-0.65 ~-2.4 {Tags:["rpg.pr.foe","rpg.pr.wheel","rpg.pr.w3"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Health:10f,attributes:[{id:"max_health",base:10f},{id:"scale",base:2.6}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..] run attribute @s minecraft:max_health base set 10
execute as @e[type=minecraft:slime,tag=rpg.pr.wheel,distance=0..] run data merge entity @s {Health:10f}
tag @s remove rpg.pr.thb0
tag @s remove rpg.pr.thb1
tag @s remove rpg.pr.thb2
tag @s remove rpg.pr.thb3
function rpg:prologue_throne/wheel/restore_up
function rpg:prologue_throne/wheel/restore_down
function rpg:prologue_throne/wheel/restore_left
function rpg:prologue_throne/wheel/restore_right
playsound minecraft:block.respawn_anchor.charge master @a[tag=rpg.pri1] ~ ~ ~ 1.5 1.2
