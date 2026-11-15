# 在执行位置开战。同一时间只允许一场。
execute if score #fight rpg_jq matches 1 run return run tellraw @s ["",{"text":"〖雅克〗","color":"#F2F2F2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已经有一场雅克战；先用 /function rpg:jacques_boss/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.center"]}
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.jqb","rpg.jqwear","rpg.jqb.new"],Silent:1b,PersistenceRequired:1b,CustomName:[{"text":"[圣殿大团长]","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":false,"italic":false}],Health:1000f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"max_health",base:1000f},{id:"attack_damage",base:1f},{id:"armor",base:10f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.8f},{id:"movement_speed",base:0.33f}],drop_chances:{mainhand:0f,offhand:0f}}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_h 1000
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_c 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_b 40
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_n 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_k 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_cb 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_sk 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] rpg_jq_busy 44
tag @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,tag=rpg.jqb.new] remove rpg.jqb.new
scoreboard players set #fight rpg_jq 1
scoreboard players set #stage rpg_jq 1
scoreboard players set #empty rpg_jq 0
scoreboard players set #tick rpg_jq 0
bossbar set rpg:jacques_boss name {"text":"\ue294\ue274\ue270\ue278","font":"rpg:jacques_boss"}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1,sort=nearest] rpg_jq_s 20
bossbar set rpg:jacques_boss max 1000
bossbar set rpg:jacques_boss value 1000
bossbar set rpg:jacques_boss visible true
function rpg:jacques_boss/music/1
particle minecraft:end_rod ~ ~1.5 ~ 0.6 1.2 0.6 0.04 40 force
function rpg:jacques_boss/vfx/intro
playsound minecraft:event.raid.horn hostile @a[distance=..48] ~ ~ ~ 2 1.2
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣殿骑士团，奉教皇之名。拔剑吧，年轻人。","color":"#9C9A94","bold":false,"italic":false}]
