# 在执行位置开战。同一时间只允许一场。
execute if score #fight rpg_lub matches 1 run return run tellraw @s ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已经有一场路西法战；先用 /function rpg:lucifer_boss/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.lub.center"]}
summon minecraft:vindicator ~ ~1 ~ {Tags:["rpg.lub","rpg.demon","rpg.lub.new"],Silent:1b,PersistenceRequired:1b,CustomName:[{"text":"[最终]","color":"#5FD68C","bold":true,"italic":false},{"text":"路西法","color":"#5FD68C","bold":false,"italic":false}],Health:1000f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b},{id:"speed",duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:"max_health",base:1000f},{id:"attack_damage",base:11f},{id:"attack_knockback",base:2f},{id:"armor",base:8f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.5f}],drop_chances:{mainhand:0f,offhand:0f}}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] rpg_lub_h 1000
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] rpg_dm_lord 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] rpg_lub 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] rpg_lub_c 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] rpg_dm_cd 60
tag @e[type=minecraft:vindicator,tag=rpg.lub,tag=rpg.lub.new] remove rpg.lub.new
scoreboard players set #fight rpg_lub 1
scoreboard players set #stage rpg_lub 1
scoreboard players set #empty rpg_lub 0
scoreboard players set #tick rpg_lub 0
bossbar set rpg:lucifer_boss name {"text":"\ue214\ue1f4\ue1f0\ue1f8","font":"rpg:lucifer_boss"}
bossbar set rpg:lucifer_boss max 1000
bossbar set rpg:lucifer_boss value 1000
bossbar set rpg:lucifer_boss visible true
function rpg:lucifer_boss/music/1
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.6} ~ ~1 ~ 1 1.5 1 0.05 80 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..48] ~ ~ ~ 1.2 0.5
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":" 𝔏𝔲𝔠𝔦𝔣𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"我是晨星，是早晨之子。你们的神给了我光，又把我摔下天来。","color":"#9C9A94","bold":false,"italic":false}]
