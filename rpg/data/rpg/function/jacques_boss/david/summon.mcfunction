summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.jqd"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"大卫的幽灵","color":"#D8ECFF","italic":false},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqd,distance=..1] rpg_jq_t 0
particle minecraft:end_rod ~ ~1 ~ 0.4 1 0.4 0.05 30
playsound minecraft:block.amethyst_block.chime hostile @a[distance=..32] ~ ~ ~ 1.4 1.2
tellraw @a[distance=..48] ["",{"text":"〖大卫〗","color":"#D8ECFF","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"你不是第一个推石头的人。","color":"#E6DFCF","bold":false,"italic":false}]
