# 天使士兵：隐身的卫道士载体套 rpg:prologue_angel（Sven 图集），手里是看不见的剑
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.pr.foe","rpg.pr.w.angel","rpg.pr.angel","rpg.pr.new"],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Rotation:[90f,0f],Health:30f,attributes:[{id:"max_health",base:30d},{id:"attack_damage",base:5d},{id:"follow_range",base:48d}],equipment:{mainhand:{id:"minecraft:iron_sword",count:1,components:{"minecraft:item_model":"rpg:empty"}}},drop_chances:{mainhand:0f},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_angel/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
