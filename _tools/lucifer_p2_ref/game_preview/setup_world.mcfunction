gamerule advance_time false
gamerule advance_weather false
gamerule spawn_mobs false
weather clear
time set midnight
forceload add -32 -32 32 32
fill -20 63 -20 20 63 20 minecraft:gray_concrete
setworldspawn 0 70 28 180
summon minecraft:vindicator 0 64 0 {Tags:["p2_client_npc","rpg.lu.phase2"],NoAI:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,Rotation:[0f,0f]}
scoreboard players set @e[tag=p2_client_npc,limit=1] rpg_dm_lord 1
execute as @e[tag=p2_client_npc,limit=1] at @s run function rpg:lucifer_p2/dress
execute as @e[tag=p2_client_npc,limit=1] at @s run function rpg:lucifer_p2/anim/jungleabomination_idle/f0
scoreboard players set @e[tag=p2_client_npc,limit=1] rpg_lu2_anim 99
execute as @e[tag=p2_client_npc,limit=1] run data merge entity @s {active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0b,show_particles:0b}]}
defaultgamemode spectator
save-all flush
