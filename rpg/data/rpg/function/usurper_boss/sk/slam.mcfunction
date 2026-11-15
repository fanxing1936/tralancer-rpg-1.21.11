scoreboard players operation #m rpg_ub = @s rpg_ub_t
scoreboard players set #k rpg_ub 4
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score @s rpg_ub_t matches ..38 if score #m rpg_ub matches 0 at @s positioned ^0.11 ^1.80 ^0.79 run function rpg:usurper_boss/slam/charge
execute if score @s rpg_ub_t matches 53 run function rpg:usurper_boss/slam/burst
execute if score @s rpg_ub_t matches 54 run execute as @e[tag=rpg.usb.sring] run data merge entity @s {start_interpolation:0,interpolation_duration:57,transformation:{scale:[40f,1f,40f]}}
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss0] at @s rotated 0 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss1] at @s rotated 30 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss2] at @s rotated 60 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss3] at @s rotated 90 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss4] at @s rotated 120 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss5] at @s rotated 150 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss6] at @s rotated 180 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss7] at @s rotated 210 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss8] at @s rotated 240 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss9] at @s rotated 270 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss10] at @s rotated 300 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 as @e[tag=rpg.usb.ss11] at @s rotated 330 0 run tp @s ^ ^ ^20
execute if score @s rpg_ub_t matches 54 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=0.00..1.05,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 55 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=0.00..1.40,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 56 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=0.35..1.75,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 57 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=0.70..2.10,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 58 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=1.05..2.45,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 59 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=1.40..2.80,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 60 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=1.75..3.15,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 61 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=2.10..3.50,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 62 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=2.45..3.85,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 63 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=2.80..4.20,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 64 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=3.15..4.55,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 65 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=3.50..4.90,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 66 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=3.85..5.25,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 67 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=4.20..5.60,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 68 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=4.55..5.95,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 69 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=4.90..6.30,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 70 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=5.25..6.65,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 71 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=5.60..7.00,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 72 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=5.95..7.35,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 73 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=6.30..7.70,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 74 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=6.65..8.05,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 75 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=7.00..8.40,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 76 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=7.35..8.75,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 77 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=7.70..9.10,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 78 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=8.05..9.45,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 79 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=8.40..9.80,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 80 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=8.75..10.15,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 81 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=9.10..10.50,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 82 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=9.45..10.85,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 83 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=9.80..11.20,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 84 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=10.15..11.55,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 85 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=10.50..11.90,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 86 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=10.85..12.25,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 87 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=11.20..12.60,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 88 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=11.55..12.95,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 89 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=11.90..13.30,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 90 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=12.25..13.65,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 91 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=12.60..14.00,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 92 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=12.95..14.35,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 93 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=13.30..14.70,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 94 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=13.65..15.05,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 95 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=14.00..15.40,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 96 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=14.35..15.75,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 97 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=14.70..16.10,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 98 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=15.05..16.45,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 99 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=15.40..16.80,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 100 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=15.75..17.15,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 101 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=16.10..17.50,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 102 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=16.45..17.85,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 103 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=16.80..18.20,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 104 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=17.15..18.55,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 105 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=17.50..18.90,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 106 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=17.85..19.25,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 107 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=18.20..19.60,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 108 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=18.55..19.95,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 109 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=18.90..20.30,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 110 at @e[type=minecraft:marker,tag=rpg.usb.slamc,limit=1] as @e[tag=rpg.unit.f,distance=19.25..20.65,tag=!rpg.usb.shit] if predicate rpg:usurper_boss/on_ground run function rpg:usurper_boss/slam/hit
execute if score @s rpg_ub_t matches 112.. run tag @e[tag=rpg.unit] remove rpg.usb.shit
execute if score @s rpg_ub_t matches 112.. run function rpg:usurper_boss/sk/end
