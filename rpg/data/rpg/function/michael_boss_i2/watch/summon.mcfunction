summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.mkw","rpg.mkb.w","rpg.mkb.wnew"],NoAI:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",CustomName:{"text":"守望者","color":"#FF3300","italic":false},Health:60f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"max_health",base:60f},{id:"knockback_resistance",base:0.6f}],drop_chances:{mainhand:0f,offhand:0f}}
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,tag=rpg.mkb.wnew,distance=0..] store result score @s rpg_mk_wt run random value 0..18
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb.w,tag=rpg.mkb.wnew,distance=0..] rpg_mk_ws 2
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,tag=rpg.mkb.wnew,distance=0..] at @s run execute facing entity @e[tag=rpg.unit.f,distance=..80,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:vindicator,tag=rpg.mkb.w,tag=rpg.mkb.wnew,distance=0..] remove rpg.mkb.wnew
function rpg:michael_boss_i2/vfx/blink
