title @a[tag=rpg.pri4] times 10 60 20
title @a[tag=rpg.pri4] subtitle {"text": "Prologue · A Thousand Years Ago", "color": "#BFB8A8", "italic": true}
title @a[tag=rpg.pri4] title {"text": "序章 · 一千年前", "color": "#E8D9B0", "bold": true}
function rpg:prologue_i4/sub/u10
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_4 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 0.0 141.0 18.0 -180.0 70.0
execute in rpg:armageddon_4 run summon minecraft:vindicator -30 81 0 {Tags:["rpg.pr.actor","rpg.pr.a.lucifer","rpg.pr.w.lucifer","rpg.pr.new"],Rotation:[-90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_lucifer/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
