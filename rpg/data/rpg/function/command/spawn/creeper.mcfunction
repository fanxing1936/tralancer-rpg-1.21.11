# Per-mob roll for a creeper variant (was 5 world-wide scans in rpg:command/tick).
execute store result score @s random run random value 1..10
execute if score @s random matches 10 run summon creeper ~ ~ ~ {powered:1,ExplosionRadius:5,Health:30,attributes:[{id:"scale",base:1.3f},{id:"max_health",base:30f}]}
execute if score @s random matches 9 run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"scale",base:0.5f},{id:"max_health",base:10f}]}
execute if score @s random matches 9 run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"scale",base:0.5f},{id:"max_health",base:10f}]}
execute if score @s random matches 9 run summon creeper ~ ~ ~ {ExplosionRadius:1.5,Health:10,fuse:10,attributes:[{id:"scale",base:0.5f},{id:"max_health",base:10f}]}
