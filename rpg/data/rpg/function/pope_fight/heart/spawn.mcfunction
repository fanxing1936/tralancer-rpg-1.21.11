# 判定体 + 模型（at 地面）。升起结束前打不到，也不算恶魔。
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.pf.heart"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:{text:"末影之心",color:"#D596F2",bold:true},active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
function rpg:heart_of_ender/spawn
tag @e[type=minecraft:armor_stand,tag=rpg.he,tag=!rpg.pf.rig,distance=..1,limit=1] add rpg.pf.rig
execute as @e[type=minecraft:vindicator,tag=rpg.pf.heart,limit=1] run function rpg:pope_fight/heart/init
