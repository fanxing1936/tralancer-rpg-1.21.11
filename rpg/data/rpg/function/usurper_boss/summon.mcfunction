# 在执行位置开战。同一时间只允许一场。
execute if score #fight rpg_ub matches 1 run return run tellraw @s ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已经有一场篡夺者战；先用 /function rpg:usurper_boss/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.usb.center"]}
function rpg:usurper_boss/altar_clear
summon minecraft:vindicator ~ ~1 ~ {Tags:["rpg.usb","rpg.demon.fly","rpg.usb.new"],Silent:1b,PersistenceRequired:1b,NoAI:0b,CustomName:[{"text":"[篡夺者]","color":"#B784D6","bold":true,"italic":false},{"text":"达里奥·所罗门","color":"#B784D6","bold":false,"italic":false}],Health:1000f,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"max_health",base:1000f},{id:"attack_damage",base:8f},{id:"armor",base:8f},{id:"follow_range",base:48f},{id:"knockback_resistance",base:0.6f},{id:"movement_speed",base:0.3f}],drop_chances:{mainhand:0f,offhand:0f}}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub 1
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_h 1000
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_c 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_b 40
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_n 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_k 0
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] rpg_ub_busy 102
tag @e[type=minecraft:vindicator,tag=rpg.usb,tag=rpg.usb.new] remove rpg.usb.new
scoreboard players set #fight rpg_ub 1
scoreboard players set #stage rpg_ub 1
scoreboard players set #empty rpg_ub 0
scoreboard players set #tick rpg_ub 0
bossbar set rpg:usurper_boss name {"text":"\ue214\ue1f4\ue1f0\ue1f8","font":"rpg:usurper_boss"}
scoreboard players set @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] rpg_ub_s 20
bossbar set rpg:usurper_boss color pink
bossbar set rpg:usurper_boss max 1000
bossbar set rpg:usurper_boss value 1000
bossbar set rpg:usurper_boss visible true
function rpg:usurper_boss/music/1
particle minecraft:enchant ~ ~1.5 ~ 1 1.5 1 1 160 force
playsound minecraft:block.enchantment_table.use hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#B784D6","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔘𝔰𝔲𝔯𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"所罗门封住了七十二柱，钥匙传到了我手里。","color":"#9C9A94","bold":false,"italic":false}]
