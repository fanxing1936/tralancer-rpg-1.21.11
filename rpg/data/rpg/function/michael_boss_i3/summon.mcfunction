# 在执行位置开战。同一时间只允许一场。
execute if score #fight rpg_mk_i3 matches 1 run return run tellraw @s ["",{"text":"〖米迦勒〗","color":"#FFD0BD","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已经有一场米迦勒战；先用 /function rpg:michael_boss_i3/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.center"]}
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.lag"]}
summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.last"]}
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.mkb","rpg.mkwear","rpg.mkb.new"],Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",CustomName:{"text":"米迦勒","color":"#FFD0BD","bold":true,"italic":false},Health:1200f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"max_health",base:1200f},{id:"attack_damage",base:1f},{id:"armor",base:12f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:1f},{id:"movement_speed",base:0.3f}],drop_chances:{mainhand:0f,offhand:0f}}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_i3 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_h 1200
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_c 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_n 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_k 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_cb 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_sk 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_so 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_ur 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_b 40
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] rpg_mk_busy 40
tag @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] add rpg.mkb.intro
tag @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,tag=rpg.mkb.new,distance=0..] remove rpg.mkb.new
scoreboard players set #fight rpg_mk_i3 1
scoreboard players set #stage rpg_mk_i3 1
scoreboard players set #empty rpg_mk_i3 0
scoreboard players set #tick rpg_mk_i3 0
scoreboard players set #w rpg_mk_i3 0
execute as @e[tag=rpg.unit,distance=0..] run scoreboard players operation @s rpg_mk_dd0 = @s rpg_mk_dd
scoreboard players reset @e[tag=rpg.unit,distance=0..] rpg_mk_fl
bossbar set rpg:michael_boss_i3 name {"text":"\ue314\ue2f4\ue2f0\ue2f8","font":"rpg:michael_boss"}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,sort=nearest,distance=0..] rpg_mk_s 20
bossbar set rpg:michael_boss_i3 max 1200
bossbar set rpg:michael_boss_i3 value 1200
bossbar set rpg:michael_boss_i3 visible true
execute unless score #pro rpg_mk_i3 matches 1 run function rpg:michael_boss_i3/music/1
execute unless score #pro rpg_mk_i3 matches 1 run function rpg:michael_boss_i3/vfx/intro
playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 2 0.6
playsound minecraft:entity.phantom.flap hostile @a[distance=..48] ~ ~ ~ 2 0.5
execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" 𝔔𝔲𝔦𝔰 𝔲𝔱 𝔇𝔢𝔲𝔰","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"在天上就有了争战。你身上有拂晓之星的气味。","color":"#9C9A94","bold":false,"italic":false}]
