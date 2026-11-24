title @a[tag=rpg.pr] times 10 60 20
title @a[tag=rpg.pr] subtitle {"text": "Prologue · A Thousand Years Ago", "color": "#BFB8A8", "italic": true}
title @a[tag=rpg.pr] title {"text": "序章 · 一千年前", "color": "#E8D9B0", "bold": true}
function rpg:prologue/sub/u10
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 0.0 141.0 18.0 -180.0 70.0
execute in rpg:armageddon run summon minecraft:vindicator -30 81 0 {Tags:["rpg.pr.actor","rpg.pr.a.lucifer","rpg.pr.w.lucifer","rpg.pr.new"],Rotation:[-90f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new] at @s run function rpg:prologue_lucifer/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new] remove rpg.pr.new
