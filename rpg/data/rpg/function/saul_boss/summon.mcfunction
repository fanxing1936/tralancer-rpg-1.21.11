# 在执行位置开战。同一时间只允许一场。
execute if score #fight rpg_sl matches 1 run return run tellraw @s ["",{"text":"〖扫罗〗","color":"#D8DEE6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已经有一场扫罗战；先用 /function rpg:saul_boss/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.center"]}
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slb","rpg.slwear","rpg.slb.new"],Silent:1b,PersistenceRequired:1b,CustomName:{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},Health:1000f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"max_health",base:1000f},{id:"attack_damage",base:1f},{id:"armor",base:14f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.8f},{id:"movement_speed",base:0.33f}],drop_chances:{mainhand:0f,offhand:0f}}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_h 1000
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_c 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_n 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_k 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_cb 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_sk 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_b 40
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] rpg_sl_busy 44
tag @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,tag=rpg.slb.new] remove rpg.slb.new
scoreboard players set #fight rpg_sl 1
scoreboard players set #stage rpg_sl 1
scoreboard players set #empty rpg_sl 0
scoreboard players set #tick rpg_sl 0
execute as @e[tag=rpg.unit] run scoreboard players operation @s rpg_sl_dd0 = @s rpg_sl_dd
bossbar set rpg:saul_boss name {"text":"\ue294\ue274\ue270\ue278","font":"rpg:saul_boss"}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1,sort=nearest] rpg_sl_s 20
bossbar set rpg:saul_boss max 1000
bossbar set rpg:saul_boss value 1000
bossbar set rpg:saul_boss visible true
function rpg:saul_boss/music/1
function rpg:saul_boss/vfx/intro
playsound minecraft:item.trident.return hostile @a[distance=..48] ~ ~ ~ 2 0.7
tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#D8DEE6","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔐𝔞𝔯𝔰𝔥𝔞𝔩","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……斯塔福德？是你吗，老伙计？好，好！拔剑，让我看看你荒废了多少。","color":"#9C9A94","bold":false,"italic":false}]
